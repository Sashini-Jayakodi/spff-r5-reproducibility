"""Standalone exact-arithmetic verification of a synthetic nonterminal-unsafe example.

LOCAL REVIEW ONLY. Institutional release rights have not been established.
No outside data or third-party research code are included.
"""
from collections import defaultdict
from fractions import Fraction
import json
from math import comb
from pathlib import Path

N = 10
SIGNATURES = [(0, 1, 2), (0, 2, 2), (1, 1, 2), (1, 2, 2)]
# Pre-established cutoffs for the frozen binomial tests at alpha=.35, delta=.10:
# stage 0: P(Bin(10,.35)<=1) <= .1 < P(Bin(10,.35)<=2)
# stage 1: P(Bin(50,.35)<=12) <= .1 < P(Bin(50,.35)<=13)
CUTOFF_0 = 1
CUTOFF_1 = 12


def exact_event_probability(t: Fraction):
    q = [t, Fraction(1, 2) - t, Fraction(1, 2) - t, t]
    assert sum(q) == 1 and all(x >= 0 for x in q)
    marg0 = sum((w for w, s in zip(q, SIGNATURES) if s[0] == 1), Fraction(0))
    marg1 = sum((w for w, s in zip(q, SIGNATURES) if s[1] == 2), Fraction(0))
    assert marg0 == marg1 == Fraction(1, 2)
    assert all(0 <= s[0] <= s[1] <= s[2] == 2 for s in SIGNATURES)
    assert all(0 <= s[1] - s[0] <= 4 and 0 <= s[2] - s[1] <= 1 for s in SIGNATURES)
    states = {(0, 0): Fraction(1)}
    for _ in range(N):
        new = defaultdict(Fraction)
        for (e0, e1), weight in states.items():
            for s, w in zip(SIGNATURES, q):
                if w:
                    new[e0 + s[0], e1 + s[1]] += weight * w
        states = new
    assert sum(states.values()) == 1
    return sum((prob for (e0, e1), prob in states.items()
                if e0 <= CUTOFF_0 and e1 > CUTOFF_1), Fraction(0))


def exact_closed_form(t: Fraction):
    """A strict-pass event has zero or one first-stage errors.
    Conditional on strict errors, the middle-stage tail is binomial.
    """
    p = 2*t
    z = 1-p
    def tail(k, thr):
        return sum((Fraction(comb(k,j))*z**j*(1-z)**(k-j)
                    for j in range(thr,k+1)), Fraction(0))
    return (tail(10,3)+10*((1-p)*tail(9,3)+p*tail(9,2)))/1024


def main():
    values = []
    for t in (Fraction(0), Fraction(1, 8), Fraction(1, 4), Fraction(3, 8), Fraction(1, 2)):
        prob = exact_event_probability(t)
        assert prob == exact_closed_form(t), (t, prob, exact_closed_form(t))
        values.append({"t_fraction": str(t), "probability_fraction": str(prob),
                       "probability": float(prob), "percentage": 100 * float(prob)})
    assert values[0]["probability_fraction"] == "11/1024"
    assert values[-1]["probability_fraction"] == "0"
    assert values[2]["probability_fraction"] == "1331/131072"
    output = {
        "scope": "physically nested fixed-count, 3 thresholds, nonterminal unsafe set",
        "status": "local mathematical verification, not independent proof review",
        "counts_per_cluster": [1, 5, 6],
        "alpha": 0.35, "delta": 0.10, "n_clusters": N,
        "first_unsafe_threshold": 0,
        "population_risks": [0.5, 0.3, 1.0 / 3],
        "stage0_max_pass_error": 1,
        "stage1_max_pass_error": 12,
        "feasible_t_interval": [0, 0.5],
        "identification_set_closed": [0.0, 11.0 / 1024.0],
        "identification_set_endpoint_attainment": ["t=1/2", "t=0"],
        "exact_points": values,
    }
    out = Path(__file__).with_name("nonterminal_exact_results.json")
    out.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
