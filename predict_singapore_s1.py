#!/usr/bin/env python3
"""
Main prediction script for PGL Major Singapore 2026 Stage 1
Generates Pick'em recommendations based on simulations and analysis
"""

import sys
from prediction_algorithm_singapore_s1 import SingaporeS1Predictor
from team_data_singapore_s1 import TEAMS_DATA_SINGAPORE_S1, ROUND_1_MATCHUPS_SINGAPORE_S1


def print_header(text: str):
    print("\n" + "=" * 80)
    print(text.center(80))
    print("=" * 80 + "\n")


def print_round1_matchups(predictor: SingaporeS1Predictor):
    print_header("ROUND 1 MATCHUPS (November 24, 2026)")

    print("All matches are Best-of-1 (BO1)\n")

    for i, (team1, team2) in enumerate(ROUND_1_MATCHUPS_SINGAPORE_S1, 1):
        data1 = TEAMS_DATA_SINGAPORE_S1[team1]
        data2 = TEAMS_DATA_SINGAPORE_S1[team2]
        prob = predictor.win_probability(team1, team2)
        print(f"Match {i}: {team1:<20} (VGS #{data1['vgs_rank']:<2}) vs {team2:<20} (VGS #{data2['vgs_rank']:<2})"
              f"  ->  {prob * 100:4.1f}% / {(1 - prob) * 100:4.1f}%")


def print_team_strengths(predictor: SingaporeS1Predictor):
    print_header("TEAM STRENGTH ANALYSIS")

    rankings = predictor.get_strength_rankings()

    print("Strength = 50% data model + 50% market (bookmaker odds to qualify for Stage 2)\n")
    print(f"{'Rank':<6} {'Team':<22} {'Strength':<10} {'Model':<8} {'Market':<8} {'Odds':<7} {'VGS':<6} {'Seed':<6} {'Momentum':<12}")
    print("-" * 80)

    for i, (team, strength) in enumerate(rankings, 1):
        data = TEAMS_DATA_SINGAPORE_S1[team]
        odds = f"{data['stage2_odds']:.2f}" if data['stage2_odds'] else "n/a"
        print(f"{i:<6} {team:<22} {strength:<10.2f} {predictor.model_strength[team]:<8.2f} "
              f"{data['market_strength']:<8.2f} {odds:<7} "
              f"#{data['vgs_rank']:<5} {data['vgs_seed']:<6} {data['momentum']:<12}")


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


def print_pickem_recommendations(predictor: SingaporeS1Predictor, results: dict):
    print_header("PICK'EM RECOMMENDATIONS")

    predictions = predictor.get_top_predictions(results)

    print("3-0 CANDIDATES (Choose 2)")
    print("-" * 80)
    for i, (team, prob) in enumerate(predictions['3-0'][:5], 1):
        data = TEAMS_DATA_SINGAPORE_S1[team]
        confidence = "HIGH" if prob > 15 else "MEDIUM" if prob > 10 else "LOW"
        print(f"\n{i}. {team} - {prob:.2f}% probability [{confidence} CONFIDENCE]")
        print(f"   VGS: #{data['vgs_rank']} | Seed: {data['vgs_seed']} | Momentum: {data['momentum']}")
        print(f"   Rationale: {data['notes']}")

    print("\n\n0-3 CANDIDATES (Choose 2)")
    print("-" * 80)
    for i, (team, prob) in enumerate(predictions['0-3'][:5], 1):
        data = TEAMS_DATA_SINGAPORE_S1[team]
        confidence = "HIGH" if prob > 15 else "MEDIUM" if prob > 10 else "LOW"
        print(f"\n{i}. {team} - {prob:.2f}% probability [{confidence} CONFIDENCE]")
        print(f"   VGS: #{data['vgs_rank']} | Seed: {data['vgs_seed']} | Momentum: {data['momentum']}")
        print(f"   Rationale: {data['notes']}")

    print("\n\nADVANCEMENT CANDIDATES (sorted by total chance to advance)")
    print("-" * 80)
    print("Total chance to reach Stage 2 (reference only - the slate below ranks by 3-1/3-2):")
    print()

    advancement_probs = []
    for team in results:
        total_advance = results[team]['3-0'] + results[team]['3-1'] + results[team]['3-2']
        advancement_probs.append((team, total_advance, results[team]))

    advancement_probs.sort(key=lambda x: x[1], reverse=True)

    for i, (team, advance_prob, probs) in enumerate(advancement_probs[:12], 1):
        print(f"{i:>2}. {team:<22} - {advance_prob:>6.2f}% to advance "
              f"(3-0: {probs['3-0']:>5.2f}% | 3-1: {probs['3-1']:>5.2f}% | 3-2: {probs['3-2']:>5.2f}%)")


def print_recommended_picks(predictor: SingaporeS1Predictor, results: dict):
    print_header("FINAL PICK'EM RECOMMENDATIONS")

    picks = predictor.get_optimal_picks(results)

    print("\nYOUR PICK'EM SLATE (maximises expected correct picks):\n")

    print("3-0 Picks (Choose 2):")
    for i, (team, prob) in enumerate(picks['3-0'], 1):
        print(f"  {i}. {team:<22} ({prob:.2f}% probability)")

    print("\n0-3 Picks (Choose 2):")
    for i, (team, prob) in enumerate(picks['0-3'], 1):
        print(f"  {i}. {team:<22} ({prob:.2f}% probability)")

    print("\nAdvancing Teams - must finish 3-1 or 3-2 (Choose 6):")
    for i, (team, prob) in enumerate(picks['advance'], 1):
        total = results[team]['3-0'] + results[team]['3-1'] + results[team]['3-2']
        print(f"  {i}. {team:<22} ({prob:.2f}% to go 3-1/3-2 | {total:.2f}% to advance)")

    print(f"\nExpected correct picks: {picks['expected_correct']:.2f} of 10")

    print("\n" + "-" * 80)
    print("\nIMPORTANT NOTES:")
    print("   * These predictions are based on statistical analysis and simulations")
    print("   * CS2 has high variance - upsets are common in Swiss format")
    print("   * Consider your own research and recent team news")
    print("   * The 3-0 and 0-3 picks are high-risk, high-reward choices")
    print("   * Stage 1 runs November 24-27, 2026")
    print("   * Top 8 teams advance to Stage 2")
    print("   * BO1 for all matches except elimination/advancement (BO3)")
    print("\nTOTAL PICKS: 2x (3-0) + 2x (0-3) + 6x (Advance) = 10 teams")


def main():
    print_header("PGL MAJOR SINGAPORE 2026 - STAGE 1 PREDICTOR")
    print("Data-driven Pick'em analysis using Valve Global Standings, form, bookmaker odds and simulations")
    print("Based on 16-team Swiss system format")
    print("All 16 teams seeded by the Valve Global Standings of November 2, 2026\n")

    print("Initializing predictor...")
    predictor = SingaporeS1Predictor()

    print_round1_matchups(predictor)

    print_team_strengths(predictor)

    print("\nRunning 10,000 Monte Carlo simulations of Swiss bracket...")
    print("Using REAL Round 1 matchups (November 24, 2026), Valve Buchholz pairing, BO3 deciders")
    print("(This may take a moment...)\n")

    results = predictor.simulate_swiss_stage(simulations=10000, first_round_matchups=ROUND_1_MATCHUPS_SINGAPORE_S1)

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
