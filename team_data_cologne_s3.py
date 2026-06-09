"""
Team data for IEM Cologne Major 2026 - Stage 3 (Legends Stage)
Data includes: HLTV rankings, Stage 2 records, recent form, expert analysis
Last updated: June 10, 2026 (after Stage 2 conclusion)
Stage 3 Format: 16-team Swiss System, ALL matches Best-of-3, top 8 advance to Playoffs
Seeding: Legends 1-8 (Valve Global Standings), Stage 2 qualifiers 9-16 (Swiss + Buchholz)
"""

TEAMS_DATA_COLOGNE_S3 = {
    # ===== LEGENDS / DIRECT INVITES (Seeds 1-8, Valve Global Standings) =====
    "Team Vitality": {
        "source": "Legend (Seed 1, VGS #1)",
        "hltv_rank": 1,
        "stage2_record": "N/A",
        "momentum": "excellent",
        "form_score": 9.5,
        "upset_potential": "low",
        "consistency": 9.5,
        "notes": "Undisputed #1, back-to-back Major champions (Austin 2025, Budapest 2025) chasing the Astralis three-peat. Five international trophies in H1 2026. ZywOo/ropz/flameZ dominant, the team to beat"
    },
    "Team Falcons": {
        "source": "Legend (Seed 2, VGS #3)",
        "hltv_rank": 4,
        "stage2_record": "N/A",
        "momentum": "good",
        "form_score": 8.0,
        "upset_potential": "low",
        "consistency": 7.0,
        "notes": "Superteam with NiKo/m0NESY/karrigan, VGS #3. Lost CS Asia Championships final 1-3 to Legacy but consistently deep at tier-1. High firepower, occasional clutch wobbles"
    },
    "Natus Vincere": {
        "source": "Legend (Seed 3, VGS #4)",
        "hltv_rank": 2,
        "stage2_record": "N/A",
        "momentum": "good",
        "form_score": 8.5,
        "upset_potential": "low",
        "consistency": 8.0,
        "notes": "HLTV #2, Aleksib-led with b1t/w0nderful/iM. Beaten only by Vitality at the very top recently. Strong structured CT sides, real title contender"
    },
    "MOUZ": {
        "source": "Legend (Seed 4, VGS #5)",
        "hltv_rank": 6,
        "stage2_record": "N/A",
        "momentum": "good",
        "form_score": 7.5,
        "upset_potential": "low",
        "consistency": 7.5,
        "notes": "Consistent top-6 with torzsi/Spinx/jL/xertioN. Lost a BO1 to TYLOO at CAC but rarely exits early in BO3. Reliable but needs a spark to win it all"
    },
    "The MongolZ": {
        "source": "Legend (Seed 5, VGS #7)",
        "hltv_rank": 7,
        "stage2_record": "N/A",
        "momentum": "good",
        "form_score": 8.0,
        "upset_potential": "low",
        "consistency": 7.5,
        "notes": "Austin 2025 Major finalists (lost to Vitality). 910/Senzu core, elite in BO3 series. Asia's best, dangerous against anyone on a good map pool"
    },
    "FURIA": {
        "source": "Legend (Seed 7, VGS #10)",
        "hltv_rank": 5,
        "stage2_record": "N/A",
        "momentum": "good",
        "form_score": 7.5,
        "upset_potential": "medium",
        "consistency": 6.5,
        "notes": "HLTV #5, led the VGS earlier in 2026. Brazilian flagship with aggressive style - high ceiling but variance-prone in long series. Home for FURIA fans in the crowd"
    },
    "PARIVISION": {
        "source": "Legend (Seed 8, VGS #16)",
        "hltv_rank": 13,
        "stage2_record": "N/A",
        "momentum": "moderate",
        "form_score": 6.5,
        "upset_potential": "high",
        "consistency": 6.0,
        "notes": "Won BLAST Bounty and hit top-3 VGS early in 2026 but slid to VGS #16 since, Jame IGL with patient control style. Lowest-seeded Legend - has the pedigree but cooled off, boom-or-bust"
    },
    "Aurora Gaming": {
        "source": "Legend (Seed 6, VGS #9)",
        "hltv_rank": 9,
        "stage2_record": "N/A",
        "momentum": "good",
        "form_score": 7.0,
        "upset_potential": "medium",
        "consistency": 6.5,
        "notes": "Turkish core, VGS #9 - highest of the lower Legend seeds. Took FUT to a thriller at PGL Cluj-Napoca. Solid mid-tier Legend that can trouble bigger names in BO3"
    },

    # ===== STAGE 2 QUALIFIERS (Seeds 9-16, Swiss + Buchholz) =====
    "FUT Esports": {
        "source": "Stage 2 (3-0)",
        "hltv_rank": 13,
        "stage2_record": "3-0",
        "momentum": "excellent",
        "form_score": 8.0,
        "upset_potential": "medium",
        "consistency": 7.0,
        "notes": "Perfect 3-0 through Stage 2, krabeni elite IGL. Carrying real momentum but R1 draw is the toughest possible - Vitality"
    },
    "Team Spirit": {
        "source": "Stage 2 (3-0)",
        "hltv_rank": 3,
        "stage2_record": "3-0",
        "momentum": "excellent",
        "form_score": 9.0,
        "upset_potential": "low",
        "consistency": 7.5,
        "notes": "3-0 in Stage 2 and HLTV #3, PGL Astana champions. Strongest qualifier by far - basically a Legend that happened to route through Stage 2. Opens vs NAVI"
    },
    "G2 Esports": {
        "source": "Stage 2 (3-1)",
        "hltv_rank": 14,
        "stage2_record": "3-1",
        "momentum": "good",
        "form_score": 7.5,
        "upset_potential": "medium",
        "consistency": 7.0,
        "notes": "3-1 in Stage 2, playoffs at last three tier-1 events. Solid but drew Falcons in R1 - a real test of their BO3 credentials"
    },
    "BetBoom": {
        "source": "Stage 2 (3-1)",
        "hltv_rank": 22,
        "stage2_record": "3-1",
        "momentum": "good",
        "form_score": 8.0,
        "upset_potential": "medium",
        "consistency": 7.0,
        "notes": "3-1 in Stage 2 carrying Stage 1 form forward, beat Vitality at IEM Atlanta earlier in 2026. Controlled chaos style, dangerous floor pick vs The MongolZ"
    },
    "9z Team": {
        "source": "Stage 2 (3-1)",
        "hltv_rank": 20,
        "stage2_record": "3-1",
        "momentum": "good",
        "form_score": 7.0,
        "upset_potential": "high",
        "consistency": 6.0,
        "notes": "Overachieving 3-1 in Stage 2 with three Major rookies, HUASOPEEK 1.10 rating. House money from here, faces PARIVISION in R1"
    },
    "Monte": {
        "source": "Stage 2 (3-2)",
        "hltv_rank": 24,
        "stage2_record": "3-2",
        "momentum": "good",
        "form_score": 6.0,
        "upset_potential": "high",
        "consistency": 5.5,
        "notes": "Survived to 3-2 in Stage 2 (2-0 over paiN). Four Major rookies playing fearless, but the lowest-rated qualifier - opens vs Aurora"
    },
    "B8": {
        "source": "Stage 2 (3-2)",
        "hltv_rank": 17,
        "stage2_record": "3-2",
        "momentum": "good",
        "form_score": 7.5,
        "upset_potential": "medium",
        "consistency": 6.5,
        "notes": "Clinched the last Stage 3 berth over BIG. Came off a Stage 1 3-0 then 3-2 in Stage 2 - proven in this Swiss format, but R1 vs FURIA is brutal"
    },
    "Legacy": {
        "source": "Stage 2 (3-2)",
        "hltv_rank": 10,
        "stage2_record": "3-2",
        "momentum": "good",
        "form_score": 7.5,
        "upset_potential": "medium",
        "consistency": 6.5,
        "notes": "CS Asia Championships 2026 champions (beat Falcons 3-1), broke into HLTV top 10. VGS #6 - underseeded as a qualifier, faces MOUZ in R1"
    }
}

ALL_TEAMS_COLOGNE_S3 = list(TEAMS_DATA_COLOGNE_S3.keys())

# INITIAL SEEDING
# Seeds 1-8: Legends by Valve Global Standings (June 2026, confirmed)
#   Vitality #1, Falcons #3, NAVI #4, MOUZ #5, MongolZ #7, Aurora #9, FURIA #10, PARIVISION #16
#   (Spirit #2 and Legacy #6 are Stage 2 qualifiers -> seeded 9-16)
# Seeds 9-16: Stage 2 qualifiers by Swiss record + Buchholz
INITIAL_SEEDING_COLOGNE_S3 = [
    "Team Vitality",        # 1  (Legend, VGS #1)
    "Team Falcons",         # 2  (Legend, VGS #3)
    "Natus Vincere",        # 3  (Legend, VGS #4)
    "MOUZ",                 # 4  (Legend, VGS #5)
    "The MongolZ",          # 5  (Legend, VGS #7)
    "Aurora Gaming",        # 6  (Legend, VGS #9)
    "FURIA",                # 7  (Legend, VGS #10)
    "PARIVISION",           # 8  (Legend, VGS #16)
    "FUT Esports",          # 9  (3-0)
    "Team Spirit",          # 10 (3-0)
    "G2 Esports",           # 11 (3-1)
    "BetBoom",              # 12 (3-1)
    "9z Team",              # 13 (3-1)
    "Monte",                # 14 (3-2)
    "B8",                   # 15 (3-2)
    "Legacy"                # 16 (3-2)
]

# OFFICIAL Round 1 Matchups (confirmed from HLTV/Liquipedia - June 11, 2026)
# ALL matches Best-of-3. Pairing: Legend (Seed 1-8) vs Stage 2 Qualifier (Seed 9-16)
ROUND_1_MATCHUPS_COLOGNE_S3 = [
    ("Team Vitality", "FUT Esports"),       # Match 1 - BO3
    ("Natus Vincere", "Team Spirit"),       # Match 2 - BO3
    ("Team Falcons", "G2 Esports"),         # Match 3 - BO3
    ("The MongolZ", "BetBoom"),             # Match 4 - BO3
    ("PARIVISION", "9z Team"),              # Match 5 - BO3
    ("MOUZ", "Legacy"),                     # Match 6 - BO3
    ("FURIA", "B8"),                        # Match 7 - BO3
    ("Aurora Gaming", "Monte")              # Match 8 - BO3
]
