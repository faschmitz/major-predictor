"""
Team data for PGL Major Singapore 2026 - Stage 2
Last updated: November 27, 2026
Stage 2 Format: 16-team Swiss System, top 8 advance to Stage 3 (Nov 28 - Dec 1, 2026)

Sources:
- Seeding: seeds 1-8 are the invited teams in Valve Global Standings order
  (official ValveSoftware/counter-strike_regional_standings file of 2026-11-02);
  seeds 9-16 are the Stage 1 qualifiers by final Stage 1 placing (Wikipedia
  standings table, sourced from HLTV). Together they reproduce all eight official
  Round 1 pairings (1v9 ... 8v16) published by HLTV/PGL.
- vgs_rank / vgs_points: same VGS snapshot (2026-11-02). Stage 1 results are not
  in it yet; they enter through form/momentum below.
- Form / notes: Stage 1 match results (Wikipedia/HLTV), Strafe, Pley, Insider
  Gaming, esport.vision and Skin.Club reports (Aug-Nov 2026).
- r1_market: Polymarket Round 1 match prices in cents (Nov 27). No bookmaker
  quoted "to qualify for Stage 3" prices for this stage, so the market input is
  the Round 1 price only. market_strength is generated from it by
  calibrate_market_singapore_s2.py - do not hand-edit.

Scoring guidelines used for the qualitative fields:
- form_score (0-10) weighs results against top-30 opposition, NOT raw win/loss.
- volatility: how swingy the team is map-to-map ("low" .. "very high"). It is
  applied symmetrically (shrinks any matchup towards 50/50).

Names: PVISION (PARIVISION) and THE ONE (1win) compete under alternate names
because of Singapore's gambling-sponsor rules.
"""

TEAMS_DATA_SINGAPORE_S2 = {
    # ------------------------------------------------------------ invited (1-8)
    "FUT": {
        "vgs_seed": 1, "vgs_rank": 8, "vgs_points": 1721,
        "s1_record": None, "r1_market": 72, "market_strength": 74.0,
        "momentum": "good",
        "form_score": 7.0,
        "volatility": "medium",
        "consistency": 6.5,
        "notes": "Seed 1 do stage. Vice-campeões da EWC em agosto (1-3 para a Spirit na final). Na BLAST Rivals de Hong Kong (nov) caíram em 7º-8º após 1-2 para a MOUZ, com xfl0ud em 1.22 de rating. Favoritos claros na estreia (72% no Polymarket)."
    },
    "Nemiga": {
        "vgs_seed": 2, "vgs_rank": 10, "vgs_points": 1650,
        "s1_record": None, "r1_market": 53, "market_strength": 75.4,
        "momentum": "very good",
        "form_score": 7.5,
        "volatility": "medium",
        "consistency": 6.5,
        "notes": "Vice-campeões do PGL Masters Bucharest (31/out), perdendo a final por 2-3 para a FURIA. No caminho eliminaram a The MongolZ e bateram a Vitality por 2-0 na semi (robo com 1.52). Em outubro perderam a final da Stake Ranked para a Astralis (1-3)."
    },
    "G2": {
        "vgs_seed": 3, "vgs_rank": 11, "vgs_points": 1616,
        "s1_record": None, "r1_market": 54, "market_strength": 64.81,
        "momentum": "moderate",
        "form_score": 5.5,
        "volatility": "medium",
        "consistency": 4.5,
        "notes": "Outono ruim: 0-3 e lanterna em Bucharest (0-2 para a NAVI na estreia) e uma vitória em nove séries até a IEM Beijing. Reagiram na BLAST Rivals de Hong Kong batendo a MOUZ (2-1) antes de cair para Spirit e Falcons. HLTV #12. Estreia contra a Liquid, ex-time do NertZ."
    },
    "THE ONE": {
        "vgs_seed": 4, "vgs_rank": 12, "vgs_points": 1598,
        "s1_record": None, "r1_market": 54, "market_strength": 65.16,
        "momentum": "good",
        "form_score": 6.0,
        "volatility": "medium",
        "consistency": 5.5,
        "notes": "1win (nafany, fame, Ax1Le, BELCHONOKK e ArtFr0st), com nome trocado pelas regras de Singapura. Na ESL Pro League (out) bateram G2, Legacy e Spirit antes de cair nas quartas para a Aurora (0-2). Campeões do Moscow Cyber Games (nov), evento regional. Não jogaram o PGL Bucharest."
    },
    "Natus Vincere": {
        "vgs_seed": 5, "vgs_rank": 13, "vgs_points": 1589,
        "s1_record": None, "r1_market": 65, "market_strength": 72.01,
        "momentum": "moderate",
        "form_score": 6.5,
        "volatility": "medium",
        "consistency": 6.0,
        "notes": "Outono irregular (derrotas para PVISION, Falcons e FURIA), mas bateram G2 (2-0) e eliminaram a Spirit em Bucharest, e foram semifinalistas da IEM Beijing (0-2 para a MongolZ). O mercado é mais otimista que o modelo: ~80% de avançar no Polymarket."
    },
    "Astralis": {
        "vgs_seed": 6, "vgs_rank": 14, "vgs_points": 1572,
        "s1_record": None, "r1_market": 56, "market_strength": 53.12,
        "momentum": "shaky",
        "form_score": 5.0,
        "volatility": "high",
        "consistency": 4.5,
        "notes": "Elenco em transição: campeões da Stake Ranked em 4/out (3-1 na Nemiga), mas cinco dias depois afastaram HooXi e jabbi. Para o Major inscreveram phzy, ryu, siuhy, Staehr e Anlelele (emprestado). Quase nenhum jogo oficial com essa formação."
    },
    "The MongolZ": {
        "vgs_seed": 7, "vgs_rank": 17, "vgs_points": 1554,
        "s1_record": None, "r1_market": 71, "market_strength": 63.61,
        "momentum": "very good",
        "form_score": 7.5,
        "volatility": "medium",
        "consistency": 6.5,
        "notes": "Vice-campeões da IEM Beijing (8/nov): bateram FURIA (2-1) e NAVI (2-0) antes de perder a final por 0-3 para a MOUZ. Saíram de Bucharest no decider contra a Nemiga. Seed baixo para a força atual."
    },
    "MIBR": {
        "vgs_seed": 8, "vgs_rank": 19, "vgs_points": 1546,
        "s1_record": None, "r1_market": 49, "market_strength": 55.24,
        "momentum": "moderate",
        "form_score": 5.0,
        "volatility": "high",
        "consistency": 5.0,
        "notes": "insani, LNZ, nqz, tomaszin e venomzera. Eliminaram a NRG na StarSeries Fall (tomaszin com 1.45), mas perderam 0-2 para a Eternal Fire no fim de outubro. Caíram no Stage 2 de Cologne. Estreia equilibrada contra a 100 Thieves."
    },
    # ------------------------------------------------- Stage 1 qualifiers (9-16)
    "FlyQuest": {
        "vgs_seed": 9, "vgs_rank": 48, "vgs_points": 1318,
        "s1_record": "3-0", "r1_market": 29, "market_strength": 54.98,
        "momentum": "very good",
        "form_score": 6.5,
        "volatility": "high",
        "consistency": 6.0,
        "notes": "1º do Stage 1 com 3-0, saindo do seed 14: bateram Eternal Fire, PVISION e Imperial (2-0). Terceiro Major seguido passando do Stage 1. jks em grande fase; aliStair de volta como AWPer/IGL. Agora o nível sobe: FUT na estreia."
    },
    "Ninjas in Pyjamas": {
        "vgs_seed": 10, "vgs_rank": 15, "vgs_points": 1564,
        "s1_record": "3-0", "r1_market": 49, "market_strength": 73.83,
        "momentum": "very good",
        "form_score": 7.5,
        "volatility": "medium",
        "consistency": 7.0,
        "notes": "3-0 no Stage 1 batendo M80, Lynn Vision e Liquid (2-0). Krimbo (IGL) com stavn e sjuush; três títulos de LAN seguidos antes do Major. Maior VGS entre os classificados. Estreia equilibrada com a Nemiga (49% x 53% no Polymarket)."
    },
    "Liquid": {
        "vgs_seed": 11, "vgs_rank": 21, "vgs_points": 1528,
        "s1_record": "3-1", "r1_market": 47, "market_strength": 62.02,
        "momentum": "good",
        "form_score": 7.5,
        "volatility": "medium",
        "consistency": 6.0,
        "notes": "3-1 no Stage 1: bateram GOSH, Wildcard e Imperial (2-0); só perderam para a NIP (0-2). Campeões do iBUYPOWER Masters no outono, com vitórias em BO3 sobre Vitality, G2, MOUZ e Aurora. Mirage e Inferno são a base."
    },
    "Eternal Fire": {
        "vgs_seed": 12, "vgs_rank": 22, "vgs_points": 1513,
        "s1_record": "3-1", "r1_market": 47, "market_strength": 62.36,
        "momentum": "good",
        "form_score": 6.5,
        "volatility": "medium",
        "consistency": 6.0,
        "notes": "3-1 no Stage 1: perderam a estreia para a FlyQuest e depois venceram DENDELE, 100 Thieves e M80 (2-1). jottAAA é a estrela. Bateram a MIBR por 2-0 em outubro. Ancient forte; não jogam Nuke."
    },
    "PVISION": {
        "vgs_seed": 13, "vgs_rank": 16, "vgs_points": 1560,
        "s1_record": "3-1", "r1_market": 36, "market_strength": 60.42,
        "momentum": "good",
        "form_score": 7.0,
        "volatility": "low",
        "consistency": 7.0,
        "notes": "PARIVISION. 3-1 no Stage 1: venceram DENDELE, FaZe e Lynn Vision (2-0); perderam só para a FlyQuest. Jame, FL1T, HObbit, xiELO e zweih. Pegam a NAVI na estreia, rival que já enfrentaram duas vezes no outono (duas séries 2-1)."
    },
    "Imperial": {
        "vgs_seed": 14, "vgs_rank": 35, "vgs_points": 1406,
        "s1_record": "3-2", "r1_market": 45, "market_strength": 48.59,
        "momentum": "good",
        "form_score": 5.0,
        "volatility": "medium",
        "consistency": 5.0,
        "notes": "3-2 no Stage 1: começaram 2-0 (HEROIC e 100 Thieves), levaram 0-2 de FlyQuest e Liquid e venceram o decider contra a Wildcard por 2-1. Time do IGL VINI, forte contra sul-americanos, ainda sem séries vencidas contra o tier 1."
    },
    "Lynn Vision": {
        "vgs_seed": 15, "vgs_rank": 56, "vgs_points": 1267,
        "s1_record": "3-2", "r1_market": 30, "market_strength": 45.61,
        "momentum": "good",
        "form_score": 5.0,
        "volatility": "high",
        "consistency": 5.0,
        "notes": "3-2 no Stage 1 saindo do seed 16: bateram 9z, Wildcard e HEROIC (2-0 no decider, EmiliaQAQ com 1.45); perderam para NIP e PVISION. Menor VGS do stage. Estreia contra a MongolZ, a outra força asiática."
    },
    "100 Thieves": {
        "vgs_seed": 16, "vgs_rank": 23, "vgs_points": 1511,
        "s1_record": "3-2", "r1_market": 52, "market_strength": 56.5,
        "momentum": "moderate",
        "form_score": 6.0,
        "volatility": "high",
        "consistency": 5.5,
        "notes": "3-2 no Stage 1: venceram Chinggis Warriors, 9z (2-1) e M80 (2-1 no decider); perderam para Imperial e Eternal Fire. device, rain e poiii, com gla1ve de coach. Dust2 muito forte, resto do mapa irregular. Leves favoritos contra a MIBR."
    },
}

# INITIAL SEEDING: invited teams by VGS (1-8), then Stage 1 placing (9-16)
INITIAL_SEEDING_SINGAPORE_S2 = sorted(
    TEAMS_DATA_SINGAPORE_S2, key=lambda t: TEAMS_DATA_SINGAPORE_S2[t]["vgs_seed"]
)

ALL_TEAMS_SINGAPORE_S2 = list(INITIAL_SEEDING_SINGAPORE_S2)

# OFFICIAL Round 1 matchups (HLTV / PGL, Nov 28, 2026) - all BO1.
ROUND_1_MATCHUPS_SINGAPORE_S2 = [
    ("FUT", "FlyQuest"),                     # 1 v 9
    ("Nemiga", "Ninjas in Pyjamas"),         # 2 v 10
    ("G2", "Liquid"),                        # 3 v 11
    ("THE ONE", "Eternal Fire"),             # 4 v 12
    ("Natus Vincere", "PVISION"),            # 5 v 13
    ("Astralis", "Imperial"),                # 6 v 14
    ("The MongolZ", "Lynn Vision"),          # 7 v 15
    ("MIBR", "100 Thieves"),                 # 8 v 16
]

assert ROUND_1_MATCHUPS_SINGAPORE_S2 == [
    (INITIAL_SEEDING_SINGAPORE_S2[i], INITIAL_SEEDING_SINGAPORE_S2[i + 8]) for i in range(8)
], "Round 1 matchups do not match the 1v9..8v16 seeding pattern"

# Polymarket "Qualify to Stage 3" prices seen on Nov 27 (only three teams listed).
# Not used by the model; printed by the calibration script as a sanity check.
POLYMARKET_ADVANCE_SINGAPORE_S2 = {
    "Natus Vincere": 0.80,
    "FUT": 0.75,
    "G2": 0.63,
}
