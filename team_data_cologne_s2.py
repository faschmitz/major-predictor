"""
Team data for IEM Cologne Major 2026 - Stage 2
Data includes: HLTV rankings, Stage 1 records, recent form, expert analysis
Last updated: June 5, 2026 (after Stage 1 conclusion)
Stage 2 Format: 16-team Swiss System, top 8 advance to Stage 3
Seeding: Invited teams 1-8 (Valve Global Standings), Stage 1 qualifiers 9-16 (Swiss + Buchholz)
"""

TEAMS_DATA_COLOGNE_S2 = {
    # ===== DIRECT INVITES (Seeds 1-8, Valve Global Standings) =====
    "FUT Esports": {
        "source": "Direct invite (Seed 4, VGS #13)",
        "hltv_rank": 12,
        "stage1_record": "N/A",
        "momentum": "good",
        "form_score": 7.5,
        "upset_potential": "medium",
        "consistency": 7.0,
        "notes": "Won recent event beating Astralis 3-1 in grand final, krabeni elite IGL (2nd best IGL rating). Sent to lower bracket by paiN and eliminated by B8 at IEM Atlanta - beatable by Stage 1 teams"
    },
    "Team Spirit": {
        "source": "Direct invite (Seed 1, VGS #2)",
        "hltv_rank": 3,
        "stage1_record": "N/A",
        "momentum": "excellent",
        "form_score": 9.0,
        "upset_potential": "low",
        "consistency": 7.5,
        "notes": "PGL Astana 2026 champions, 20-7 (74.1%) recent record, 5-1 vs NAVI, 5-2 vs MOUZ. Roster changes paid off but consistency remains the question mark. Clear strongest team in Stage 2"
    },
    "Astralis": {
        "source": "Direct invite (Seed 3, VGS #12)",
        "hltv_rank": 10,
        "stage1_record": "N/A",
        "momentum": "good",
        "form_score": 8.0,
        "upset_potential": "low",
        "consistency": 7.5,
        "notes": "Reached grand final of recent event (lost 3-1 to FUT), solid top-10 HLTV ranking. Danish core stable, strong BO1 team but 3-1 vs Spirit head-to-head is negative"
    },
    "G2 Esports": {
        "source": "Direct invite (Seed 5, VGS #14)",
        "hltv_rank": 13,
        "stage1_record": "N/A",
        "momentum": "good",
        "form_score": 7.5,
        "upset_potential": "low",
        "consistency": 7.0,
        "notes": "Playoffs at last three tier-1 tournaments, 5th at PGL Astana 2026, 70% win rate over last 30 days. Reliable advancement pick but not a title contender right now"
    },
    "Legacy": {
        "source": "Direct invite (Seed 2, VGS #6)",
        "hltv_rank": 18,
        "stage1_record": "N/A",
        "momentum": "good",
        "form_score": 7.5,
        "upset_potential": "medium",
        "consistency": 6.5,
        "notes": "CS Asia Championships 2026 champions beating Falcons 3-1 in the grand final - VGS #6 (1856 pts). HLTV slower to credit (#18) but proven tier-1 ceiling, leading Brazilian contingent outside FURIA"
    },
    "paiN Gaming": {
        "source": "Direct invite (Seed 6, VGS #18)",
        "hltv_rank": 19,
        "stage1_record": "N/A",
        "momentum": "moderate",
        "form_score": 6.5,
        "upset_potential": "medium",
        "consistency": 6.0,
        "notes": "Secured playoffs at IEM Atlanta sending FUT to lower bracket, but dropped to #19 HLTV. Budapest Major Legends experience, capable of beating anyone on a good day"
    },
    "Monte": {
        "source": "Direct invite (Seed 8, VGS #24)",
        "hltv_rank": 20,
        "stage1_record": "N/A",
        "momentum": "moderate",
        "form_score": 6.0,
        "upset_potential": "high",
        "consistency": 5.5,
        "notes": "Four Major rookies (afro, Gizmy, AZUWU, Rainwaker) plus Bymas returning. Grinded from lower VRS ranks since mid-2025, unproven at this level - volatile in both directions"
    },
    "9z Team": {
        "source": "Direct invite (Seed 7, VGS #20)",
        "hltv_rank": 16,
        "stage1_record": "N/A",
        "momentum": "good",
        "form_score": 7.0,
        "upset_potential": "medium",
        "consistency": 6.0,
        "notes": "Biggest riser in spring rankings (jumped 5 spots in April), HUASOPEEK posting 1.10 rating. Three Major rookies but momentum is real - dangerous floor pick"
    },

    # ===== STAGE 1 QUALIFIERS (Seeds 9-16, Swiss + Buchholz) =====
    "B8": {
        "source": "Stage 1 (3-0)",
        "hltv_rank": 17,
        "stage1_record": "3-0",
        "momentum": "excellent",
        "form_score": 8.5,
        "upset_potential": "low",
        "consistency": 7.5,
        "notes": "Perfect 3-0 run through Stage 1 including 13-6 over TYLOO. Confirmed IEM Atlanta form (eliminated FUT there), s1zzi questions answered for now"
    },
    "BetBoom": {
        "source": "Stage 1 (3-0)",
        "hltv_rank": 22,
        "stage1_record": "3-0",
        "momentum": "excellent",
        "form_score": 9.0,
        "upset_potential": "low",
        "consistency": 8.0,
        "notes": "Dominant 3-0 in Stage 1 (13-4 vs Gaimin, swept GamerLegion 2-0). Beat Vitality at IEM Atlanta, controlled chaos style peaking at the right time"
    },
    "GamerLegion": {
        "source": "Stage 1 (3-1)",
        "hltv_rank": 14,
        "stage1_record": "3-1",
        "momentum": "excellent",
        "form_score": 8.5,
        "upset_potential": "low",
        "consistency": 8.0,
        "notes": "3-1 in Stage 1, only loss to red-hot BetBoom. IEM Atlanta grand finalists, REZ/PR/Tauson elite rifling, hypex clutch AWPer. Strongest qualifier on paper"
    },
    "M80": {
        "source": "Stage 1 (3-1)",
        "hltv_rank": 21,
        "stage1_record": "3-1",
        "momentum": "good",
        "form_score": 7.0,
        "upset_potential": "medium",
        "consistency": 6.5,
        "notes": "Solid 3-1 run including win over NRG. Rediscovering 2025 form when it matters, but ceiling against tier-1 invites unproven"
    },
    "MIBR": {
        "source": "Stage 1 (3-1)",
        "hltv_rank": 26,
        "stage1_record": "3-1",
        "momentum": "good",
        "form_score": 8.0,
        "upset_potential": "medium",
        "consistency": 7.0,
        "notes": "3-1 in Stage 1, eased past Lynn Vision to qualify. Carrying CAC/Bucharest form forward, insani star rifler in great shape"
    },
    "TYLOO": {
        "source": "Stage 1 (3-2)",
        "hltv_rank": 23,
        "stage1_record": "3-2",
        "momentum": "good",
        "form_score": 6.5,
        "upset_potential": "high",
        "consistency": 5.5,
        "notes": "Lost R1 to B8 13-6 but fought through lower bracket (2-0 SINNERS, 2-0 Lynn Vision). BO3 resilience shown, but BO1 inconsistency remains a risk"
    },
    "BIG": {
        "source": "Stage 1 (3-2)",
        "hltv_rank": 30,
        "stage1_record": "3-2",
        "momentum": "good",
        "form_score": 6.5,
        "upset_potential": "medium",
        "consistency": 6.0,
        "notes": "3-2 with hard-fought loss to GamerLegion along the way. Home crowd at LANXESS Arena is real fuel, blameF leadership and gr1ks AWP trending up"
    },
    "FlyQuest": {
        "source": "Stage 1 (3-2)",
        "hltv_rank": 56,
        "stage1_record": "3-2",
        "momentum": "good",
        "form_score": 5.5,
        "upset_potential": "high",
        "consistency": 4.5,
        "notes": "Biggest Stage 1 surprise - popular 0-3 pick that went 3-2, stamping out Liquid 2-0 to qualify. Confidence sky-high but weakest team on paper in Stage 2"
    }
}

ALL_TEAMS_COLOGNE_S2 = list(TEAMS_DATA_COLOGNE_S2.keys())

# INITIAL SEEDING
# Seeds 1-8: Direct invites by Valve Global Standings (confirmed June 2026):
#   Spirit #2, Legacy #6, Astralis #12, FUT #13, G2 #14, paiN #18, 9z #20, Monte #24
# Seeds 9-16: Stage 1 qualifiers by Swiss record + Buchholz
INITIAL_SEEDING_COLOGNE_S2 = [
    "Team Spirit",          # 1  (invite, VGS #2)
    "Legacy",               # 2  (invite, VGS #6)
    "Astralis",             # 3  (invite, VGS #12)
    "FUT Esports",          # 4  (invite, VGS #13)
    "G2 Esports",           # 5  (invite, VGS #14)
    "paiN Gaming",          # 6  (invite, VGS #18)
    "9z Team",              # 7  (invite, VGS #20)
    "Monte",                # 8  (invite, VGS #24)
    "B8",                   # 9  (3-0)
    "BetBoom",              # 10 (3-0)
    "GamerLegion",          # 11 (3-1)
    "M80",                  # 12 (3-1)
    "MIBR",                 # 13 (3-1)
    "TYLOO",                # 14 (3-2)
    "BIG",                  # 15 (3-2)
    "FlyQuest"              # 16 (3-2)
]

# OFFICIAL Round 1 Matchups (confirmed from HLTV/Liquipedia - June 5, 2026)
# Fixed list used as-is for Round 1; rounds 2+ pair by seed within record groups
ROUND_1_MATCHUPS_COLOGNE_S2 = [
    ("FUT Esports", "B8"),              # Match 1 - BO1
    ("Team Spirit", "BetBoom"),         # Match 2 - BO1
    ("Astralis", "GamerLegion"),        # Match 3 - BO1
    ("G2 Esports", "M80"),              # Match 4 - BO1
    ("Legacy", "MIBR"),                 # Match 5 - BO1
    ("paiN Gaming", "TYLOO"),           # Match 6 - BO1
    ("Monte", "BIG"),                   # Match 7 - BO1
    ("9z Team", "FlyQuest")             # Match 8 - BO1
]
