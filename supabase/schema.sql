-- ============================================================================
-- Bolão do Major - esquema do banco (Supabase / Postgres)
--
-- Como usar: no painel do Supabase, abra "SQL Editor", cole este arquivo
-- inteiro e clique em "Run". Pode rodar mais de uma vez sem perder dados.
--
-- A chave pública (anon / publishable) fica exposta na página, então TODAS as
-- regras do bolão são garantidas aqui, e não no JavaScript:
--   * palpites só podem ser gravados antes do horário de trava do stage;
--   * ninguém lê o palpite dos outros antes da trava;
--   * um palpite precisa ter 2 + 2 + 6 times distintos, todos do stage;
--   * só administradores gravam resultados e horário de trava;
--   * só se entra em um grupo com o código de convite.
-- ============================================================================

-- ---------------------------------------------------------------------------
-- Tabelas
-- ---------------------------------------------------------------------------

create table if not exists public.profiles (
    id           uuid primary key references auth.users (id) on delete cascade,
    display_name text not null
                 check (char_length(btrim(display_name)) between 2 and 24),
    created_at   timestamptz not null default now()
);

-- Administradores ficam em tabela separada, sem nenhuma permissão de escrita
-- para os usuários: ninguém consegue se promover pela API.
create table if not exists public.admins (
    user_id uuid primary key references auth.users (id) on delete cascade
);

create table if not exists public.stages (
    id         text primary key,
    name       text not null,
    teams      text[] not null,          -- em ordem de seed
    lock_at    timestamptz not null,     -- início da primeira partida
    results    jsonb not null default '{}'::jsonb
               check (jsonb_typeof(results) = 'object'),  -- {"Time": [vitórias, derrotas]}
    updated_at timestamptz not null default now()
);

create table if not exists public.groups (
    id          uuid primary key default gen_random_uuid(),
    name        text not null check (char_length(btrim(name)) between 2 and 40),
    invite_code text not null unique,
    owner_id    uuid not null references auth.users (id) on delete cascade,
    created_at  timestamptz not null default now()
);

create table if not exists public.group_members (
    group_id  uuid not null references public.groups (id) on delete cascade,
    user_id   uuid not null references auth.users (id) on delete cascade,
    joined_at timestamptz not null default now(),
    primary key (group_id, user_id)
);
create index if not exists group_members_user_idx on public.group_members (user_id);

create table if not exists public.picks (
    user_id    uuid not null references auth.users (id) on delete cascade,
    stage_id   text not null references public.stages (id) on delete cascade,
    three_zero text[] not null,
    zero_three text[] not null,
    advance    text[] not null,
    updated_at timestamptz not null default now(),
    primary key (user_id, stage_id)
);

-- ---------------------------------------------------------------------------
-- Funções auxiliares (security definer para não cair em recursão de RLS)
-- ---------------------------------------------------------------------------

create or replace function public.is_admin()
returns boolean
language sql stable security definer set search_path = ''
as $$
    select exists (select 1 from public.admins a where a.user_id = auth.uid());
$$;

create or replace function public.is_member(p_group uuid)
returns boolean
language sql stable security definer set search_path = ''
as $$
    select exists (
        select 1 from public.group_members m
        where m.group_id = p_group and m.user_id = auth.uid()
    );
$$;

create or replace function public.shares_group(p_user uuid)
returns boolean
language sql stable security definer set search_path = ''
as $$
    select exists (
        select 1
        from public.group_members mine
        join public.group_members theirs on theirs.group_id = mine.group_id
        where mine.user_id = auth.uid() and theirs.user_id = p_user
    );
$$;

create or replace function public.stage_locked(p_stage text)
returns boolean
language sql stable security definer set search_path = ''
as $$
    select coalesce((select now() >= s.lock_at from public.stages s where s.id = p_stage), true);
$$;

-- ---------------------------------------------------------------------------
-- Gatilhos
-- ---------------------------------------------------------------------------

-- Cria o perfil junto com a conta, usando o nome informado no cadastro.
create or replace function public.handle_new_user()
returns trigger
language plpgsql security definer set search_path = ''
as $$
declare
    v_name text;
begin
    v_name := left(btrim(coalesce(new.raw_user_meta_data ->> 'display_name', '')), 24);
    if char_length(v_name) < 2 then
        v_name := 'Jogador';
    end if;
    insert into public.profiles (id, display_name)
    values (new.id, v_name)
    on conflict (id) do nothing;
    return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
    after insert on auth.users
    for each row execute function public.handle_new_user();

-- Valida e trava os palpites.
create or replace function public.check_picks()
returns trigger
language plpgsql security definer set search_path = ''
as $$
declare
    v_stage public.stages%rowtype;
    v_all   text[];
begin
    if tg_op = 'UPDATE' and (new.user_id <> old.user_id or new.stage_id <> old.stage_id) then
        raise exception 'Não é possível mover um palpite.' using errcode = 'check_violation';
    end if;

    select * into v_stage from public.stages s where s.id = new.stage_id;
    if not found then
        raise exception 'Stage desconhecido.' using errcode = 'check_violation';
    end if;
    if now() >= v_stage.lock_at then
        raise exception 'Palpites encerrados: o stage já começou.' using errcode = 'check_violation';
    end if;

    if coalesce(array_ndims(new.three_zero), 0) <> 1 or coalesce(array_ndims(new.zero_three), 0) <> 1
       or coalesce(array_ndims(new.advance), 0) <> 1
       or cardinality(new.three_zero) <> 2 or cardinality(new.zero_three) <> 2
       or cardinality(new.advance) <> 6 then
        raise exception 'O palpite precisa de 2 times 3-0, 2 times 0-3 e 6 que avançam.'
            using errcode = 'check_violation';
    end if;

    v_all := new.three_zero || new.zero_three || new.advance;
    if array_position(v_all, null) is not null
       or (select count(distinct t) from unnest(v_all) as t) <> 10 then
        raise exception 'Cada time só pode aparecer uma vez no palpite.' using errcode = 'check_violation';
    end if;
    if not (v_all <@ v_stage.teams) then
        raise exception 'O palpite contém um time que não está neste stage.' using errcode = 'check_violation';
    end if;

    new.updated_at := now();
    return new;
end;
$$;

drop trigger if exists picks_check on public.picks;
create trigger picks_check
    before insert or update on public.picks
    for each row execute function public.check_picks();

create or replace function public.touch_stage()
returns trigger
language plpgsql set search_path = ''
as $$
begin
    new.updated_at := now();
    return new;
end;
$$;

drop trigger if exists stages_touch on public.stages;
create trigger stages_touch
    before update on public.stages
    for each row execute function public.touch_stage();

-- ---------------------------------------------------------------------------
-- Funções chamadas pela página (RPC)
-- ---------------------------------------------------------------------------

create or replace function public.create_group(p_name text)
returns public.groups
language plpgsql security definer set search_path = ''
as $$
declare
    v_uid   uuid := auth.uid();
    v_group public.groups;
    v_code  text;
begin
    if v_uid is null then
        raise exception 'Entre na sua conta primeiro.' using errcode = 'insufficient_privilege';
    end if;
    if char_length(btrim(coalesce(p_name, ''))) not between 2 and 40 then
        raise exception 'O nome do grupo precisa ter de 2 a 40 caracteres.' using errcode = 'check_violation';
    end if;
    if (select count(*) from public.groups g where g.owner_id = v_uid) >= 20 then
        raise exception 'Limite de 20 grupos criados por pessoa.' using errcode = 'check_violation';
    end if;

    loop
        v_code := upper(substr(replace(gen_random_uuid()::text, '-', ''), 1, 8));
        exit when not exists (select 1 from public.groups g where g.invite_code = v_code);
    end loop;

    insert into public.groups (name, invite_code, owner_id)
    values (btrim(p_name), v_code, v_uid)
    returning * into v_group;

    insert into public.group_members (group_id, user_id) values (v_group.id, v_uid);
    return v_group;
end;
$$;

create or replace function public.join_group(p_code text)
returns public.groups
language plpgsql security definer set search_path = ''
as $$
declare
    v_uid   uuid := auth.uid();
    v_group public.groups;
begin
    if v_uid is null then
        raise exception 'Entre na sua conta primeiro.' using errcode = 'insufficient_privilege';
    end if;
    select * into v_group from public.groups g
    where g.invite_code = upper(btrim(coalesce(p_code, '')));
    if not found then
        raise exception 'Código de convite inválido.' using errcode = 'no_data_found';
    end if;
    insert into public.group_members (group_id, user_id)
    values (v_group.id, v_uid)
    on conflict do nothing;
    return v_group;
end;
$$;

-- Placar de um grupo. Antes da trava devolve só quem já enviou; os times
-- escolhidos pelos outros só aparecem depois que o stage começa.
create or replace function public.group_board(p_group uuid, p_stage text)
returns table (
    user_id      uuid,
    display_name text,
    submitted    boolean,
    updated_at   timestamptz,
    three_zero   text[],
    zero_three   text[],
    advance      text[]
)
language plpgsql stable security definer set search_path = ''
as $$
declare
    v_uid    uuid := auth.uid();
    v_locked boolean := public.stage_locked(p_stage);
begin
    if v_uid is null or not public.is_member(p_group) then
        raise exception 'Você não faz parte deste grupo.' using errcode = 'insufficient_privilege';
    end if;
    return query
    select m.user_id,
           pr.display_name,
           (pk.user_id is not null),
           pk.updated_at,
           case when v_locked or m.user_id = v_uid then pk.three_zero end,
           case when v_locked or m.user_id = v_uid then pk.zero_three end,
           case when v_locked or m.user_id = v_uid then pk.advance end
    from public.group_members m
    join public.profiles pr on pr.id = m.user_id
    left join public.picks pk on pk.user_id = m.user_id and pk.stage_id = p_stage
    where m.group_id = p_group
    order by pr.display_name;
end;
$$;

-- ---------------------------------------------------------------------------
-- Permissões e RLS
-- ---------------------------------------------------------------------------

alter table public.profiles      enable row level security;
alter table public.admins        enable row level security;
alter table public.stages        enable row level security;
alter table public.groups        enable row level security;
alter table public.group_members enable row level security;
alter table public.picks         enable row level security;

revoke all on public.profiles, public.admins, public.stages, public.groups,
              public.group_members, public.picks
       from anon, authenticated;

grant select                         on public.profiles      to authenticated;
grant update (display_name)          on public.profiles      to authenticated;
grant select                         on public.admins        to authenticated;
grant select                         on public.stages        to anon, authenticated;
grant update (lock_at, results)      on public.stages        to authenticated;
grant select, delete                 on public.groups        to authenticated;
grant select, delete                 on public.group_members to authenticated;
grant select                         on public.picks         to authenticated;
grant insert (user_id, stage_id, three_zero, zero_three, advance) on public.picks to authenticated;
grant update (three_zero, zero_three, advance)                    on public.picks to authenticated;

drop policy if exists profiles_select on public.profiles;
create policy profiles_select on public.profiles for select to authenticated
    using (id = (select auth.uid()) or public.shares_group(id));

drop policy if exists profiles_update on public.profiles;
create policy profiles_update on public.profiles for update to authenticated
    using (id = (select auth.uid())) with check (id = (select auth.uid()));

drop policy if exists admins_select on public.admins;
create policy admins_select on public.admins for select to authenticated
    using (user_id = (select auth.uid()));

drop policy if exists stages_select on public.stages;
create policy stages_select on public.stages for select to anon, authenticated
    using (true);

drop policy if exists stages_update on public.stages;
create policy stages_update on public.stages for update to authenticated
    using (public.is_admin()) with check (public.is_admin());

drop policy if exists groups_select on public.groups;
create policy groups_select on public.groups for select to authenticated
    using (public.is_member(id));

drop policy if exists groups_delete on public.groups;
create policy groups_delete on public.groups for delete to authenticated
    using (owner_id = (select auth.uid()));

drop policy if exists members_select on public.group_members;
create policy members_select on public.group_members for select to authenticated
    using (public.is_member(group_id));

drop policy if exists members_leave on public.group_members;
create policy members_leave on public.group_members for delete to authenticated
    using (user_id = (select auth.uid()));

drop policy if exists picks_select on public.picks;
create policy picks_select on public.picks for select to authenticated
    using (
        user_id = (select auth.uid())
        or (public.stage_locked(stage_id) and public.shares_group(user_id))
    );

drop policy if exists picks_insert on public.picks;
create policy picks_insert on public.picks for insert to authenticated
    with check (user_id = (select auth.uid()));

drop policy if exists picks_update on public.picks;
create policy picks_update on public.picks for update to authenticated
    using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));

revoke all on function public.is_admin()                  from public, anon;
revoke all on function public.is_member(uuid)             from public, anon;
revoke all on function public.shares_group(uuid)          from public, anon;
revoke all on function public.stage_locked(text)          from public;
revoke all on function public.create_group(text)          from public, anon;
revoke all on function public.join_group(text)            from public, anon;
revoke all on function public.group_board(uuid, text)     from public, anon;
revoke all on function public.handle_new_user()           from public, anon, authenticated;
revoke all on function public.check_picks()               from public, anon, authenticated;

grant execute on function public.is_admin()               to authenticated;
grant execute on function public.is_member(uuid)          to authenticated;
grant execute on function public.shares_group(uuid)       to authenticated;
grant execute on function public.stage_locked(text)       to anon, authenticated;
grant execute on function public.create_group(text)       to authenticated;
grant execute on function public.join_group(text)         to authenticated;
grant execute on function public.group_board(uuid, text)  to authenticated;

-- ---------------------------------------------------------------------------
-- Stage atual: PGL Major Singapore 2026 - Stage 1
-- Trava: 24/nov/2026 12:00 em Singapura (01:00 de Brasília, 04:00 UTC).
-- ---------------------------------------------------------------------------

insert into public.stages (id, name, teams, lock_at)
values (
    'singapore_s1',
    'PGL Major Singapore 2026 · Stage 1',
    array[
        'Ninjas in Pyjamas', 'PVISION', 'HEROIC', 'FaZe',
        'Liquid', 'Eternal Fire', '100 Thieves', '9z',
        'M80', 'DENDELE', 'Imperial', 'Wildcard',
        'GOSH', 'FlyQuest', 'Chinggis Warriors', 'Lynn Vision'
    ],
    '2026-11-24T04:00:00Z'
)
on conflict (id) do nothing;

-- Depois de criar a sua conta na página, rode UMA vez (trocando o e-mail)
-- para virar administrador e poder lançar os resultados:
--
--   insert into public.admins (user_id)
--   select id from auth.users where email = 'seu-email@exemplo.com';
