"""
Prediction algorithm for PGL Major Singapore 2026 Stage 1

Differences from the Cologne predictors (bugs found in the review):
- Swiss pairing follows the Valve Major rulebook: mid-stage seed = record, then
  difficulty score (Buchholz), then initial seed; rounds 2-3 pair highest vs
  lowest seed avoiding rematches; rounds 4-5 use Valve's 15-row priority table.
- Advancement/elimination matches are simulated as BO3, the rest as BO1.
- Matchup probability is symmetric: P(A beats B) == 1 - P(B beats A).
- Rank input is the Valve Global Standing points (complete and official for all
  16 teams) instead of a partially available HLTV rank.
- Simulation is seeded, so the terminal script and the HTML page agree.
- Bookmaker odds to qualify for Stage 2 are blended in (MARKET_WEIGHT): the pure
  data model was much sharper than the market. `market_strength` in the team
  data is fitted by calibrate_market_singapore_s1.py.
"""

import random
from typing import Dict, List, Optional, Tuple

from team_data_singapore_s1 import (
    TEAMS_DATA_SINGAPORE_S1,
    ALL_TEAMS_SINGAPORE_S1,
    INITIAL_SEEDING_SINGAPORE_S1,
)

DEFAULT_SEED = 20261124
RECORDS = ['3-0', '3-1', '3-2', '2-3', '1-3', '0-3']

MOMENTUM_SCORES = {
    'excellent': 95,
    'very good': 85,
    'good': 75,
    'moderate': 60,
    'shaky': 45,
    'poor': 30,
}

# How much a matchup is pulled towards 50/50 (average of both teams).
VOLATILITY_SHRINK = {
    'low': 0.00,
    'medium': 0.05,
    'high': 0.10,
    'very high': 0.15,
}

# Strength difference -> single-map win probability: 1 / (1 + 10^(-diff / SCALE)).
LOGISTIC_SCALE = 44

# Final strength = (1 - w) * model strength + w * market-implied strength.
MARKET_WEIGHT = 0.5

# Valve Major Supplemental Rulebook - priority table for six-team groups
# (rounds 4 and 5). First row without a rematch is used. Seeds are 0-indexed.
PRIORITY_TABLE = [
    ((0, 5), (1, 4), (2, 3)),
    ((0, 5), (1, 3), (2, 4)),
    ((0, 4), (1, 5), (2, 3)),
    ((0, 4), (1, 3), (2, 5)),
    ((0, 3), (1, 5), (2, 4)),
    ((0, 3), (1, 4), (2, 5)),
    ((0, 5), (1, 2), (3, 4)),
    ((0, 4), (1, 2), (3, 5)),
    ((0, 2), (1, 5), (3, 4)),
    ((0, 2), (1, 4), (3, 5)),
    ((0, 3), (1, 2), (4, 5)),
    ((0, 2), (1, 3), (4, 5)),
    ((0, 1), (2, 5), (3, 4)),
    ((0, 1), (2, 4), (3, 5)),
    ((0, 1), (2, 3), (4, 5)),
]


class SingaporeS1Predictor:
    """
    Predicts outcomes for PGL Major Singapore 2026 Stage 1 using weighted factors:
    - Valve Global Standing points (35%)
    - Recent form vs quality opposition (30%)
    - Momentum (20%)
    - Consistency (15%)
    """

    def __init__(self, market_weight: float = MARKET_WEIGHT):
        self.teams = TEAMS_DATA_SINGAPORE_S1
        self.market_weight = market_weight
        self.weights = {
            'rank': 0.35,
            'form': 0.30,
            'momentum': 0.20,
            'consistency': 0.15,
        }
        self._seed_index = {t: i for i, t in enumerate(INITIAL_SEEDING_SINGAPORE_S1)}
        self.model_strength = {t: self._compute_model_strength(t) for t in ALL_TEAMS_SINGAPORE_S1}
        self.set_strengths({
            t: round((1 - market_weight) * self.model_strength[t] +
                     market_weight * (self.teams[t].get('market_strength') or self.model_strength[t]), 2)
            for t in ALL_TEAMS_SINGAPORE_S1
        })

    def set_strengths(self, strengths: Dict[str, float]):
        """Override team strengths (used by the market calibration script)."""
        self._strength = dict(strengths)
        self._map_prob = {
            (a, b): self._compute_map_probability(a, b)
            for a in ALL_TEAMS_SINGAPORE_S1 for b in ALL_TEAMS_SINGAPORE_S1 if a != b
        }

    # ------------------------------------------------------------------ strength

    def _compute_model_strength(self, team: str) -> float:
        data = self.teams[team]

        # VGS points are an Elo-like scale; 1200 -> 0, 1600 -> 100
        rank_score = min(100, max(0, (data['vgs_points'] - 1200) / 4))
        form_score = data['form_score'] * 10
        momentum_score = MOMENTUM_SCORES[data['momentum']]
        consistency_score = data['consistency'] * 10

        total = (
            rank_score * self.weights['rank'] +
            form_score * self.weights['form'] +
            momentum_score * self.weights['momentum'] +
            consistency_score * self.weights['consistency']
        )
        return round(total, 2)

    def calculate_team_strength(self, team: str) -> float:
        """Overall team strength score (model blended with market). Higher = stronger."""
        return self._strength[team]

    def get_strength_rankings(self) -> List[Tuple[str, float]]:
        return sorted(self._strength.items(), key=lambda x: x[1], reverse=True)

    # --------------------------------------------------------------- probability

    def _compute_map_probability(self, team1: str, team2: str) -> float:
        diff = self._strength[team1] - self._strength[team2]
        prob = 1 / (1 + 10 ** (-diff / LOGISTIC_SCALE))
        shrink = (VOLATILITY_SHRINK[self.teams[team1]['volatility']] +
                  VOLATILITY_SHRINK[self.teams[team2]['volatility']]) / 2
        return 0.5 + (prob - 0.5) * (1 - shrink)

    def win_probability(self, team1: str, team2: str, best_of: int = 1) -> float:
        """Probability that team1 beats team2 (symmetric)."""
        p = self._map_prob[(team1, team2)]
        if best_of == 3:
            return p * p * (3 - 2 * p)
        return p

    def predict_matchup(self, team1: str, team2: str, best_of: int = 1) -> Tuple[str, float]:
        """Returns (favourite, win_probability)."""
        p = self.win_probability(team1, team2, best_of)
        return (team1, p) if p >= 0.5 else (team2, 1 - p)

    # ------------------------------------------------------------------- pairing

    def _seed_order(self, group: List[str], records: Dict, opponents: Dict) -> List[str]:
        """Mid-stage seeding: difficulty score (Buchholz) desc, then initial seed."""
        def difficulty(team):
            return sum(records[o]['wins'] - records[o]['losses'] for o in opponents[team])
        return sorted(group, key=lambda t: (-difficulty(t), self._seed_index[t]))

    @staticmethod
    def _pair_high_low(ordered: List[str], opponents: Dict) -> Optional[List[Tuple[str, str]]]:
        """Highest seed faces the lowest seed available that is not a rematch."""
        if not ordered:
            return []
        top = ordered[0]
        for i in range(len(ordered) - 1, 0, -1):
            other = ordered[i]
            if other in opponents[top]:
                continue
            rest = SingaporeS1Predictor._pair_high_low(ordered[1:i] + ordered[i + 1:], opponents)
            if rest is not None:
                return [(top, other)] + rest
        return None

    def _create_swiss_pairings(self, records: Dict, active_teams: set, opponents: Dict,
                               round_num: int) -> List[Tuple[str, str]]:
        by_record: Dict[Tuple[int, int], List[str]] = {}
        for team in active_teams:
            by_record.setdefault((records[team]['wins'], records[team]['losses']), []).append(team)

        matchups = []
        for record in sorted(by_record, reverse=True):
            ordered = self._seed_order(by_record[record], records, opponents)
            pairs = None
            if round_num >= 4 and len(ordered) == 6:
                for row in PRIORITY_TABLE:
                    if all(ordered[b] not in opponents[ordered[a]] for a, b in row):
                        pairs = [(ordered[a], ordered[b]) for a, b in row]
                        break
            else:
                pairs = self._pair_high_low(ordered, opponents)
            if pairs is None:  # rematch unavoidable ("if possible" in the rulebook)
                n = len(ordered)
                pairs = [(ordered[i], ordered[n - 1 - i]) for i in range(n // 2)]
            matchups.extend(pairs)
        return matchups

    # ---------------------------------------------------------------- simulation

    def simulate_swiss_stage(self, simulations: int = 10000, first_round_matchups=None,
                             seed: Optional[int] = DEFAULT_SEED,
                             stats: Optional[dict] = None) -> Dict[str, Dict[str, float]]:
        """
        Monte Carlo simulation of the Swiss stage.
        Returns the probability (in %) of each final record per team.
        `stats`, if given, is filled with diagnostic counters (rematches, bo3 count).
        """
        rng = random.Random(seed)
        results = {team: {r: 0 for r in RECORDS} for team in ALL_TEAMS_SINGAPORE_S1}
        if stats is not None:
            stats.update({'rematches': 0, 'matches': 0, 'bo3': 0})

        for _ in range(simulations):
            records = {team: {'wins': 0, 'losses': 0} for team in ALL_TEAMS_SINGAPORE_S1}
            opponents = {team: [] for team in ALL_TEAMS_SINGAPORE_S1}
            active_teams = set(ALL_TEAMS_SINGAPORE_S1)

            round_num = 1
            while active_teams:
                if round_num == 1 and first_round_matchups is not None:
                    matchups = first_round_matchups
                else:
                    matchups = self._create_swiss_pairings(records, active_teams, opponents, round_num)

                outcomes = []
                for team1, team2 in matchups:
                    # Advancement (2 wins) and elimination (2 losses) matches are BO3
                    decisive = records[team1]['wins'] == 2 or records[team1]['losses'] == 2
                    prob1 = self.win_probability(team1, team2, 3 if decisive else 1)
                    if stats is not None:
                        stats['matches'] += 1
                        stats['bo3'] += decisive
                        stats['rematches'] += team2 in opponents[team1]
                    if rng.random() < prob1:
                        outcomes.append((team1, team2))
                    else:
                        outcomes.append((team2, team1))

                for winner, loser in outcomes:
                    records[winner]['wins'] += 1
                    records[loser]['losses'] += 1
                    opponents[winner].append(loser)
                    opponents[loser].append(winner)
                    if records[winner]['wins'] == 3:
                        active_teams.discard(winner)
                    if records[loser]['losses'] == 3:
                        active_teams.discard(loser)

                round_num += 1

            for team in ALL_TEAMS_SINGAPORE_S1:
                results[team][f"{records[team]['wins']}-{records[team]['losses']}"] += 1

        for team in ALL_TEAMS_SINGAPORE_S1:
            for record in results[team]:
                results[team][record] = round((results[team][record] / simulations) * 100, 2)

        return results

    # --------------------------------------------------------------------- picks

    def get_top_predictions(self, results: Dict) -> Dict[str, List[Tuple[str, float]]]:
        predictions = {}
        for outcome in ['3-0', '3-1', '3-2', '0-3']:
            predictions[outcome] = sorted(
                ((team, results[team][outcome]) for team in ALL_TEAMS_SINGAPORE_S1),
                key=lambda x: x[1], reverse=True)
        return predictions

    def get_optimal_picks(self, results: Dict) -> Dict[str, List[Tuple[str, float]]]:
        """
        Pick'em slate (2x 3-0, 2x 0-3, 6x advance) maximising the expected number
        of correct picks. An "advance" pick only scores if the team goes 3-1 or
        3-2 - a team that goes 3-0 does NOT count - so advance picks are ranked
        by P(3-1) + P(3-2), not by total advancement probability.
        """
        teams = ALL_TEAMS_SINGAPORE_S1
        adv = {t: results[t]['3-1'] + results[t]['3-2'] for t in teams}
        best = None
        for i, a in enumerate(teams):
            for b in teams[i + 1:]:
                for j, c in enumerate(teams):
                    if c in (a, b):
                        continue
                    for d in teams[j + 1:]:
                        if d in (a, b):
                            continue
                        rest = sorted((t for t in teams if t not in (a, b, c, d)),
                                      key=lambda t: adv[t], reverse=True)[:6]
                        score = (results[a]['3-0'] + results[b]['3-0'] +
                                 results[c]['0-3'] + results[d]['0-3'] +
                                 sum(adv[t] for t in rest))
                        if best is None or score > best[0]:
                            best = (score, (a, b), (c, d), rest)
        score, three_zero, zero_three, advance = best
        return {
            '3-0': sorted(((t, results[t]['3-0']) for t in three_zero), key=lambda x: -x[1]),
            '0-3': sorted(((t, results[t]['0-3']) for t in zero_three), key=lambda x: -x[1]),
            'advance': [(t, round(adv[t], 2)) for t in advance],
            'expected_correct': round(score / 100, 2),
        }
