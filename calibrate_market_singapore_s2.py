#!/usr/bin/env python3
"""
Fits `market_strength` for PGL Major Singapore 2026 Stage 2.

Unlike Stage 1, no bookmaker quoted "to qualify for Stage 3" prices, so the
market input is the Round 1 match price (Polymarket, `r1_market`, in cents).
For each Round 1 pair the margin is removed and the strength gap that
reproduces that single-map probability is solved exactly (inverting the same
logistic + volatility shrink used by the predictor). The pair keeps the average
of its two model strengths, so the market only moves teams relative to their
Round 1 opponent; levels across pairs still come from the data model.

Run again whenever r1_market changes:  python3 calibrate_market_singapore_s2.py
"""

import math
import re

from prediction_algorithm_singapore_s2 import (
    SingaporeS2Predictor, LOGISTIC_SCALE, VOLATILITY_SHRINK,
)
from team_data_singapore_s2 import (
    TEAMS_DATA_SINGAPORE_S2, ALL_TEAMS_SINGAPORE_S2, ROUND_1_MATCHUPS_SINGAPORE_S2,
    POLYMARKET_ADVANCE_SINGAPORE_S2,
)

DATA_FILE = "team_data_singapore_s2.py"


def strength_gap(p_map, shrink):
    """Strength difference that yields single-map probability p_map."""
    raw = 0.5 + (p_map - 0.5) / (1 - shrink)
    raw = min(max(raw, 0.02), 0.98)
    return LOGISTIC_SCALE * math.log10(raw / (1 - raw))


def fit():
    model = SingaporeS2Predictor(market_weight=0).model_strength
    strengths, targets = {}, {}
    for a, b in ROUND_1_MATCHUPS_SINGAPORE_S2:
        pa, pb = TEAMS_DATA_SINGAPORE_S2[a]['r1_market'], TEAMS_DATA_SINGAPORE_S2[b]['r1_market']
        p = pa / (pa + pb)
        shrink = (VOLATILITY_SHRINK[TEAMS_DATA_SINGAPORE_S2[a]['volatility']] +
                  VOLATILITY_SHRINK[TEAMS_DATA_SINGAPORE_S2[b]['volatility']]) / 2
        gap = strength_gap(p, shrink)
        mid = (model[a] + model[b]) / 2
        strengths[a], strengths[b] = round(mid + gap / 2, 2), round(mid - gap / 2, 2)
        targets[a], targets[b] = p, 1 - p
    return strengths, targets, model


def main():
    strengths, targets, model = fit()

    check = SingaporeS2Predictor(market_weight=0)
    check.set_strengths(strengths)
    print(f"{'Team':<20}{'R1 mkt':>8}{'target':>9}{'fitted':>9}{'market_str':>12}{'model_str':>11}")
    for a, b in ROUND_1_MATCHUPS_SINGAPORE_S2:
        for t, o in ((a, b), (b, a)):
            fitted = check.win_probability(t, o)
            print(f"{t:<20}{TEAMS_DATA_SINGAPORE_S2[t]['r1_market']:>7}c{targets[t]*100:>8.1f}%"
                  f"{fitted*100:>8.1f}%{strengths[t]:>12.2f}{model[t]:>11.2f}")

    # Sanity check against the few "qualify to Stage 3" prices that exist
    res = check.simulate_swiss_stage(20000, ROUND_1_MATCHUPS_SINGAPORE_S2)
    print("\nMarket-only simulation vs Polymarket 'qualify to Stage 3':")
    for t, p in POLYMARKET_ADVANCE_SINGAPORE_S2.items():
        adv = res[t]['3-0'] + res[t]['3-1'] + res[t]['3-2']
        print(f"  {t:<18} sim {adv:5.1f}%   Polymarket {p*100:.0f}%")

    src = open(DATA_FILE, encoding="utf-8").read()
    for t, s in strengths.items():
        pat = re.compile(r'("%s": \{\n.*?"market_strength": )[^,\n]+' % re.escape(t), re.S)
        src, n = pat.subn(lambda m: m.group(1) + str(s), src, count=1)
        assert n == 1, t
    open(DATA_FILE, "w", encoding="utf-8").write(src)
    print(f"\nmarket_strength written to {DATA_FILE}")


if __name__ == "__main__":
    main()
