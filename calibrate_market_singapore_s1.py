#!/usr/bin/env python3
"""
Fits `market_strength` for PGL Major Singapore 2026 Stage 1.

Finds, for each team, the strength value that makes the simulated probability
of advancing match the bookmakers' (de-vigged) odds to qualify for Stage 2,
and writes the values into team_data_singapore_s1.py.

Run again whenever stage2_odds change:  python3 calibrate_market_singapore_s1.py
"""

import math
import re

from prediction_algorithm_singapore_s1 import SingaporeS1Predictor
from team_data_singapore_s1 import (
    TEAMS_DATA_SINGAPORE_S1, ALL_TEAMS_SINGAPORE_S1, ROUND_1_MATCHUPS_SINGAPORE_S1,
)

DATA_FILE = "team_data_singapore_s1.py"
# Overround assumed for the one team without a quoted price (see market_targets)
ASSUMED_MISSING_IMPLIED = 0.70


def market_targets():
    """De-vigged probability of advancing per team (sums to 8 teams)."""
    implied = {t: (1 / d['stage2_odds'] if d['stage2_odds'] else None)
               for t, d in TEAMS_DATA_SINGAPORE_S1.items()}
    missing = [t for t, v in implied.items() if v is None]
    total = sum(v for v in implied.values() if v is not None) + ASSUMED_MISSING_IMPLIED * len(missing)
    factor = 8 / total
    return {t: (v if v is not None else ASSUMED_MISSING_IMPLIED) * factor for t, v in implied.items()}


def logit(p):
    p = min(max(p, 0.002), 0.998)
    return math.log(p / (1 - p))


def fit(iterations=40, simulations=20000):
    predictor = SingaporeS1Predictor(market_weight=0)
    targets = market_targets()
    strengths = dict(predictor.model_strength)
    for it in range(iterations):
        predictor.set_strengths(strengths)
        res = predictor.simulate_swiss_stage(simulations, ROUND_1_MATCHUPS_SINGAPORE_S1)
        adv = {t: (res[t]['3-0'] + res[t]['3-1'] + res[t]['3-2']) / 100 for t in ALL_TEAMS_SINGAPORE_S1}
        err = max(abs(adv[t] - targets[t]) for t in ALL_TEAMS_SINGAPORE_S1)
        if err < 0.01:
            break
        for t in ALL_TEAMS_SINGAPORE_S1:
            strengths[t] += 8 * (logit(targets[t]) - logit(adv[t]))
    # anchor: same average as the model strengths, so the blend is not shifted
    shift = (sum(predictor.model_strength.values()) - sum(strengths.values())) / len(strengths)
    return {t: round(s + shift, 2) for t, s in strengths.items()}, targets, adv, err


def main():
    strengths, targets, adv, err = fit()
    print(f"{'Team':<22}{'odds':>6}{'target':>9}{'fitted':>9}{'market_str':>12}{'model_str':>11}")
    model = SingaporeS1Predictor(market_weight=0).model_strength
    for t in ALL_TEAMS_SINGAPORE_S1:
        o = TEAMS_DATA_SINGAPORE_S1[t]['stage2_odds']
        print(f"{t:<22}{(o or 0):>6.2f}{targets[t]*100:>8.1f}%{adv[t]*100:>8.1f}%{strengths[t]:>12.2f}{model[t]:>11.2f}")
    print(f"max abs error: {err*100:.2f} pp")

    src = open(DATA_FILE, encoding="utf-8").read()
    for t, s in strengths.items():
        pat = re.compile(r'("%s": \{\n.*?"market_strength": )[^,\n]+' % re.escape(t), re.S)
        src, n = pat.subn(lambda m: m.group(1) + str(s), src, count=1)
        assert n == 1, t
    open(DATA_FILE, "w", encoding="utf-8").write(src)
    print(f"market_strength written to {DATA_FILE}")


if __name__ == "__main__":
    main()
