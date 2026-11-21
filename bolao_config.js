// Configuração do bolão.
// Preencha com os dados do seu projeto no Supabase (Project Settings > API).
// A chave abaixo é a PÚBLICA (anon / publishable): ela pode ficar no site.
// Nunca coloque aqui a chave "service_role" / "secret".
window.BOLAO_CONFIG = {
    supabaseUrl: "https://lacbieknadsjhyyebsim.supabase.co",
    supabaseAnonKey: "sb_publishable_J8TV-rr1PBypOLv4i1L_jw_UfjclRtF",

    // Stage em disputa (id da tabela "stages" do banco).
    stageId: "singapore_s1",
    predictionsPage: "singapore_s1.html",

    // Mostra "Esqueci a senha". Deixe false enquanto o projeto usar o e-mail
    // padrão do Supabase, que só entrega para membros do próprio projeto.
    passwordReset: false,

    // Palpite do modelo, mostrado no ranking como referência depois da trava.
    modelPicks: {
        three_zero: ["PVISION", "Ninjas in Pyjamas"],
        zero_three: ["Chinggis Warriors", "Lynn Vision"],
        advance: ["Liquid", "100 Thieves", "HEROIC", "Eternal Fire", "FaZe", "M80"]
    }
};
