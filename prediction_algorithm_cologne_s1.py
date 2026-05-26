"""
Prediction algorithm for IEM Cologne Major 2026 Stage 1
Uses multiple weighted factors to predict Swiss system outcomes
"""

import random
from typing import Dict, List, Tuple
from team_data_cologne_s1 import TEAMS_DATA_COLOGNE_S1, ALL_TEAMS_COLOGNE_S1, INITIAL_SEEDING_COLOGNE_S1


class CologneS1Predictor:
    """
    Predicts outcomes for IEM Cologne Major 2026 Stage 1 using weighted factors:
    - HLTV ranking (35%)
    - Recent form/momentum (30%)
    - Momentum/VRS standing (20%)
    - Consistency score (15%)
    """

    def __init__(self):
        self.teams = TEAMS_DATA_COLOGNE_S1
        self.weights = {
            'rank': 0.35,
            'form': 0.30,
            'momentum': 0.20,
            'consistency': 0.15
        }

    def calculate_team_strength(self, team: str) -> float:
        """
        Calculate overall team strength score (0-100)
        Higher score = stronger team
        """
        data = self.teams[team]

        rank_score = max(10, 100 - (data['hltv_rank'] * 1.25))

        form_score = data['form_score'] * 10

        if data['momentum'] == 'excellent':
            momentum_score = 95
        elif data['momentum'] == 'very good':
            momentum_score = 85
        elif data['momentum'] == 'good':
            momentum_score = 75
        elif data['momentum'] == 'moderate':
            momentum_score = 60
        elif data['momentum'] == 'shaky':
            momentum_score = 45
        else:  # poor
            momentum_score = 30

        consistency_score = data['consistency'] * 10

        total_score = (
            rank_score * self.weights['rank'] +
            form_score * self.weights['form'] +
            momentum_score * self.weights['momentum'] +
            consistency_score * self.weights['consistency']
        )

        return round(total_score, 2)

    def get_strength_rankings(self) -> List[Tuple[str, float]]:
        rankings = []
        for team in ALL_TEAMS_COLOGNE_S1:
            strength = self.calculate_team_strength(team)
            rankings.append((team, strength))

        rankings.sort(key=lambda x: x[1], reverse=True)
        return rankings

    def predict_matchup(self, team1: str, team2: str) -> Tuple[str, float]:
        strength1 = self.calculate_team_strength(team1)
        strength2 = self.calculate_team_strength(team2)

        diff = strength1 - strength2
        prob1 = 1 / (1 + 10 ** (-diff / 25))

        upset_factor = self.teams[team2]['upset_potential']
        if upset_factor == 'very high':
            prob1 *= 0.90
        elif upset_factor == 'high':
            prob1 *= 0.93
        elif upset_factor == 'medium':
            prob1 *= 0.97

        if prob1 > 0.5:
            return (team1, prob1)
        else:
            return (team2, 1 - prob1)

    def simulate_swiss_stage(self, simulations: int = 10000, first_round_matchups=None) -> Dict[str, Dict[str, float]]:
        results = {team: {'3-0': 0, '3-1': 0, '3-2': 0, '2-3': 0, '1-3': 0, '0-3': 0}
                   for team in ALL_TEAMS_COLOGNE_S1}

        for _ in range(simulations):
            records = {team: {'wins': 0, 'losses': 0} for team in ALL_TEAMS_COLOGNE_S1}
            active_teams = set(ALL_TEAMS_COLOGNE_S1)

            round_num = 1
            while active_teams:
                if round_num == 1 and first_round_matchups is not None:
                    matchups = first_round_matchups
                else:
                    matchups = self._create_swiss_pairings(records, active_teams)

                for team1, team2 in matchups:
                    winner, prob = self.predict_matchup(team1, team2)

                    if random.random() < prob:
                        records[winner]['wins'] += 1
                        loser = team2 if winner == team1 else team1
                        records[loser]['losses'] += 1
                    else:
                        loser = winner
                        winner = team2 if winner == team1 else team1
                        records[winner]['wins'] += 1
                        records[loser]['losses'] += 1

                    if records[winner]['wins'] == 3:
                        active_teams.discard(winner)
                    if records[loser]['losses'] == 3:
                        active_teams.discard(loser)

                round_num += 1

            for team in ALL_TEAMS_COLOGNE_S1:
                wins = records[team]['wins']
                losses = records[team]['losses']
                record = f"{wins}-{losses}"
                results[team][record] += 1

        for team in ALL_TEAMS_COLOGNE_S1:
            for record in results[team]:
                results[team][record] = round((results[team][record] / simulations) * 100, 2)

        return results

    def _create_swiss_pairings(self, records: Dict, active_teams: set) -> List[Tuple[str, str]]:
        by_record = {}
        for team in active_teams:
            record = (records[team]['wins'], records[team]['losses'])
            if record not in by_record:
                by_record[record] = []
            by_record[record].append(team)

        matchups = []
        for record_group in by_record.values():
            record_group.sort(key=lambda team: INITIAL_SEEDING_COLOGNE_S1.index(team))

            n = len(record_group)
            for i in range(n // 2):
                matchups.append((record_group[i], record_group[n - 1 - i]))

        return matchups

    def get_top_predictions(self, results: Dict) -> Dict[str, List[Tuple[str, float]]]:
        predictions = {
            '3-0': [],
            '3-1': [],
            '3-2': [],
            '0-3': []
        }

        for team in ALL_TEAMS_COLOGNE_S1:
            for outcome in ['3-0', '3-1', '3-2', '0-3']:
                prob = results[team][outcome]
                predictions[outcome].append((team, prob))

        for outcome in predictions:
            predictions[outcome].sort(key=lambda x: x[1], reverse=True)

        return predictions
