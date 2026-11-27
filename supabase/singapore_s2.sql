-- ============================================================================
-- Bolão do Major - abertura do Stage 2 (PGL Major Singapore 2026)
--
-- Cole no "SQL Editor" do Supabase e clique em "Run". Pode rodar mais de uma
-- vez: o Stage 2 só é criado se ainda não existir e os resultados do Stage 1
-- são sempre regravados com o placar final.
-- ============================================================================

-- 1. Resultado final do Stage 1 (fonte: tabela da Wikipedia/HLTV, 27/nov).
update public.stages
set results = '{
    "FlyQuest": [3, 0], "Ninjas in Pyjamas": [3, 0],
    "Liquid": [3, 1], "Eternal Fire": [3, 1], "PVISION": [3, 1],
    "Imperial": [3, 2], "Lynn Vision": [3, 2], "100 Thieves": [3, 2],
    "M80": [2, 3], "Wildcard": [2, 3], "HEROIC": [2, 3],
    "9z": [1, 3], "FaZe": [1, 3], "Chinggis Warriors": [1, 3],
    "DENDELE": [0, 3], "GOSH": [0, 3]
}'::jsonb
where id = 'singapore_s1';

-- 2. Stage 2. Trava: 28/nov/2026 12:00 em Singapura (01:00 de Brasília, 04:00 UTC).
insert into public.stages (id, name, teams, lock_at)
values (
    'singapore_s2',
    'PGL Major Singapore 2026 · Stage 2',
    array[
        'FUT', 'Nemiga', 'G2', 'THE ONE',
        'Natus Vincere', 'Astralis', 'The MongolZ', 'MIBR',
        'FlyQuest', 'Ninjas in Pyjamas', 'Liquid', 'Eternal Fire',
        'PVISION', 'Imperial', 'Lynn Vision', '100 Thieves'
    ],
    '2026-11-28T04:00:00Z'
)
on conflict (id) do nothing;

-- Conferência: deve listar os dois stages, o 1 com 16 resultados.
select id, lock_at, (select count(*) from jsonb_object_keys(results)) as resultados
from public.stages order by id;
