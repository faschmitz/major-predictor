// Configuração do bolão.
// Preencha com os dados do seu projeto no Supabase (Project Settings > API).
// A chave abaixo é a PÚBLICA (anon / publishable): ela pode ficar no site.
// Nunca coloque aqui a chave "service_role" / "secret".
window.BOLAO_CONFIG = {
    supabaseUrl: "https://lacbieknadsjhyyebsim.supabase.co",
    supabaseAnonKey: "sb_publishable_J8TV-rr1PBypOLv4i1L_jw_UfjclRtF",

    // Mostra "Esqueci a senha". Deixe false enquanto o projeto usar o e-mail
    // padrão do Supabase, que só entrega para membros do próprio projeto.
    passwordReset: false,

    // Stages do bolão, em ordem. O último é o que abre por padrão.
    // "id" precisa existir na tabela "stages" do banco; um stage que ainda não
    // foi criado lá é simplesmente ignorado pela página.
    // "modelPicks" é o palpite do modelo, mostrado como referência no ranking
    // depois da trava (os nomes precisam ser iguais aos do banco).
    stages: [
        {
            id: "singapore_s1",
            label: "Stage 1",
            predictionsPage: "singapore_s1.html",
            modelPicks: {
                three_zero: ["PVISION", "Ninjas in Pyjamas"],
                zero_three: ["Chinggis Warriors", "Lynn Vision"],
                advance: ["Liquid", "100 Thieves", "HEROIC", "Eternal Fire", "FaZe", "M80"]
            }
        },
        {
            id: "singapore_s2",
            label: "Stage 2",
            predictionsPage: "singapore_s2.html",
            modelPicks: {
                three_zero: ["FUT", "The MongolZ"],
                zero_three: ["Lynn Vision", "Imperial"],
                advance: ["Nemiga", "Ninjas in Pyjamas", "Natus Vincere", "THE ONE", "PVISION", "Liquid"]
            }
        }
    ]
};
