#!/usr/bin/env python3
"""
Main prediction script for IEM Cologne Major 2026 Stage 2
Generates Pick'em recommendations based on simulations and analysis
"""

import sys
from prediction_algorithm_cologne_s2 import CologneS2Predictor
from team_data_cologne_s2 import TEAMS_DATA_COLOGNE_S2, ROUND_1_MATCHUPS_COLOGNE_S2


def print_header(text: str):
    print("\n" + "=" * 80)
    print(text.center(80))
    print("=" * 80 + "\n")


def print_round1_matchups():
    print_header("ROUND 1 MATCHUPS (June 6, 2026)")

    print("All matches are Best-of-1 (BO1)")
    print("Pairing: Invite (Seed 1-8) vs Stage 1 Qualifier (Seed 9-16)\n")

    for i, (team1, team2) in enumerate(ROUND_1_MATCHUPS_COLOGNE_S2, 1):
        data1 = TEAMS_DATA_COLOGNE_S2[team1]
        data2 = TEAMS_DATA_COLOGNE_S2[team2]
        print(f"Match {i}: {team1:<20} (#{data1['hltv_rank']:<2}) vs {team2:<20} (#{data2['hltv_rank']:<2})")


def print_team_strengths(predictor: CologneS2Predictor):
    print_header("TEAM STRENGTH ANALYSIS")

    rankings = predictor.get_strength_rankings()

    print(f"{'Rank':<6} {'Team':<22} {'Strength':<12} {'HLTV':<8} {'Stage 1':<10} {'Momentum':<15}")
    print("-" * 80)

    for i, (team, strength) in enumerate(rankings, 1):
        data = TEAMS_DATA_COLOGNE_S2[team]
        print(f"{i:<6} {team:<22} {strength:<12.2f} "
              f"#{data['hltv_rank']:<7} {data['stage1_record']:<10} {data['momentum']:<15}")


def print_simulation_results(results: dict):
    print_header("SIMULATION RESULTS (10,000 iterations)")

    print(f"{'Team':<22} {'3-0':<10} {'3-1':<10} {'3-2':<10} {'2-3':<10} {'1-3':<10} {'0-3':<10}")
    print("-" * 92)

    sorted_teams = sorted(results.items(),
                         key=lambda x: x[1]['3-0'] + x[1]['3-1'] + x[1]['3-2'],
                         reverse=True)

    for team, probs in sorted_teams:
        print(f"{team:<22} "
              f"{probs['3-0']:>6.2f}%   "
              f"{probs['3-1']:>6.2f}%   "
              f"{probs['3-2']:>6.2f}%   "
              f"{probs['2-3']:>6.2f}%   "
              f"{probs['1-3']:>6.2f}%   "
              f"{probs['0-3']:>6.2f}%")


def print_pickem_recommendations(predictor: CologneS2Predictor, results: dict):
    print_header("PICK'EM RECOMMENDATIONS")

    predictions = predictor.get_top_predictions(results)

    print("3-0 CANDIDATES (Choose 2)")
    print("-" * 80)
    for i, (team, prob) in enumerate(predictions['3-0'][:5], 1):
        data = TEAMS_DATA_COLOGNE_S2[team]
        confidence = "HIGH" if prob > 15 else "MEDIUM" if prob > 10 else "LOW"
        print(f"\n{i}. {team} - {prob:.2f}% probability [{confidence} CONFIDENCE]")
        print(f"   Rank: #{data['hltv_rank']} | Stage 1: {data['stage1_record']} | Momentum: {data['momentum']}")
        print(f"   Rationale: {data['notes']}")

    print("\n\n0-3 CANDIDATES (Choose 2)")
    print("-" * 80)
    for i, (team, prob) in enumerate(predictions['0-3'][:5], 1):
        data = TEAMS_DATA_COLOGNE_S2[team]
        confidence = "HIGH" if prob > 15 else "MEDIUM" if prob > 10 else "LOW"
        print(f"\n{i}. {team} - {prob:.2f}% probability [{confidence} CONFIDENCE]")
        print(f"   Rank: #{data['hltv_rank']} | Stage 1: {data['stage1_record']} | Momentum: {data['momentum']}")
        print(f"   Rationale: {data['notes']}")

    print("\n\nADVANCEMENT CANDIDATES (3-1 or 3-2)")
    print("-" * 80)
    print("Choose 6 teams most likely to advance to Stage 3:")
    print()

    advancement_probs = []
    for team in results:
        total_advance = results[team]['3-0'] + results[team]['3-1'] + results[team]['3-2']
        advancement_probs.append((team, total_advance, results[team]))

    advancement_probs.sort(key=lambda x: x[1], reverse=True)

    for i, (team, advance_prob, probs) in enumerate(advancement_probs[:12], 1):
        print(f"{i:>2}. {team:<22} - {advance_prob:>6.2f}% to advance "
              f"(3-0: {probs['3-0']:>5.2f}% | 3-1: {probs['3-1']:>5.2f}% | 3-2: {probs['3-2']:>5.2f}%)")


def print_recommended_picks(predictor: CologneS2Predictor, results: dict):
    print_header("FINAL PICK'EM RECOMMENDATIONS")

    predictions = predictor.get_top_predictions(results)

    print("\nYOUR PICK'EM SLATE:\n")

    print("3-0 Picks (Choose 2):")
    for i in range(2):
        team, prob = predictions['3-0'][i]
        print(f"  {i+1}. {team:<22} ({prob:.2f}% probability)")

    print("\n0-3 Picks (Choose 2):")
    for i in range(2):
        team, prob = predictions['0-3'][i]
        print(f"  {i+1}. {team:<22} ({prob:.2f}% probability)")

    print("\nAdvancing Teams (Choose 6):")

    top_3_0_teams = {predictions['3-0'][0][0], predictions['3-0'][1][0]}

    advancement_probs = []
    for team in results:
        if team not in top_3_0_teams:
            total_advance = results[team]['3-0'] + results[team]['3-1'] + results[team]['3-2']
            advancement_probs.append((team, total_advance))

    advancement_probs.sort(key=lambda x: x[1], reverse=True)

    for i, (team, prob) in enumerate(advancement_probs[:6], 1):
        print(f"  {i}. {team:<22} ({prob:.2f}% to advance)")

    print("\n" + "-" * 80)
    print("\nIMPORTANT NOTES:")
    print("   * These predictions are based on statistical analysis and simulations")
    print("   * CS2 has high variance - upsets are common in Swiss format")
    print("   * Consider your own research and recent team news")
    print("   * The 3-0 and 0-3 picks are high-risk, high-reward choices")
    print("   * Stage 2 runs June 6-9, 2026")
    print("   * Top 8 teams advance to Stage 3 (Legends Stage)")
    print("   * BO1 for all matches except elimination/advancement (BO3)")
    print("\nTOTAL PICKS: 2x (3-0) + 2x (0-3) + 6x (Advance) = 10 teams")


def main():
    print_header("IEM COLOGNE MAJOR 2026 - STAGE 2 PREDICTOR")
    print("Data-driven Pick'em analysis using HLTV rankings, form, and simulations")
    print("Based on 16-team Swiss system format")
    print("Invites seeded 1-8 (Valve Global Standings), qualifiers 9-16 (Stage 1 Swiss + Buchholz)\n")

    print("Initializing predictor...")
    predictor = CologneS2Predictor()

    print_round1_matchups()

    print_team_strengths(predictor)

    print("\nRunning 10,000 Monte Carlo simulations of Swiss bracket...")
    print("Using REAL Round 1 matchups from HLTV (June 6, 2026)")
    print("(This may take a moment...)\n")

    results = predictor.simulate_swiss_stage(simulations=10000, first_round_matchups=ROUND_1_MATCHUPS_COLOGNE_S2)

    print_simulation_results(results)

    print_pickem_recommendations(predictor, results)

    print_recommended_picks(predictor, results)

    print("\n" + "=" * 80)
    print("Good luck with your Pick'ems!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrediction interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nErro: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
