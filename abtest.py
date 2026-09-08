# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas"]
# ///
"""Shared helpers for the Meridian homepage-dek A/B test notebooks.

Lives in one file so the variance formula exists once. A clustered standard error
copy-pasted into two notebooks is the single most dangerous kind of duplication in
this project: both copies look right, and a divergence between them is invisible.
"""
import math
import pandas as pd

Z95 = 1.959963985

# ---- fixed in Step 1, before any data existed -----------------------------
PLAN = {
    "baseline_ctr":          0.341,   # documented pre-test baseline
    "ship_threshold_rel":    0.05,    # business bar for rolling out
    "power_target_rel":      0.02,    # smallest effect the test can reliably detect
    "alpha":                 0.05,    # one efficacy analysis, full alpha
    "intended_alloc_b":      0.48,    # A 52 / B 48
    "coverage_gate":         0.85,    # dek coverage launch gate
    "design_effect_assumed": 1.24,    # clustering buffer used for sample sizing
    "gr_ctr_rel":           -0.05,    # guardrail: CTR harm
    "gr_ctr_hard_rel":      -0.10,    # guardrail: hard override
    "gr_bounce_pp":          0.03,    # guardrail: bounce rate rise
    "gr_churn_rel":          0.10,    # guardrail: churn non-inferiority margin
}

# analysis dates from the plan, as day numbers from launch
HEALTH_CHECK_DAY = 22      # Oct 13 — no efficacy decision available
DECISION_DAY     = 35      # Oct 27 — the single efficacy analysis


def load(path="ab_test_sessions.csv"):
    return pd.read_csv(path, parse_dates=["session_date"])


def rates(frame, by="variant", metric="clicked"):
    g = frame.groupby(by)[metric].agg(sessions="size", conversions="sum")
    g["ctr"] = g.conversions / g.sessions
    return g


def naive_se(p, n):
    """Binomial SE — assumes every row is an independent observation."""
    return math.sqrt(p * (1 - p) / n)


def clustered_se(frame, unit="user_id", metric="clicked"):
    """Delta-method SE for a ratio metric clustered on `unit`.

    The primary KPI is clicks/sessions, but assignment is sticky per user, so
    sessions within a user are correlated. Each unit contributes n_i sessions and
    k_i conversions:

        Var(p) = 1/(M * nbar^2) * 1/(M-1) * sum_i (k_i - p*n_i)^2
    """
    g = frame.groupby(unit)[metric].agg(n="size", k="sum")
    M, nbar = len(g), g.n.mean()
    p = g.k.sum() / g.n.sum()
    v = ((g.k - p * g.n) ** 2).sum() / (M - 1)
    return math.sqrt(v / (M * nbar ** 2))


def two_sided_p(z):
    return math.erfc(abs(z) / math.sqrt(2))


def compare(frame, clustered=True, group="variant", a="A", b="B",
            unit="user_id", metric="clicked", z=Z95):
    """Compare arm `b` against arm `a` on `metric`. Returns a dict.

    `clustered=True` uses the user-level delta-method SE (correct for this design).
    `clustered=False` uses the naive binomial SE — what a calculator returns when
    handed session counts, and what the peeking demo holds fixed.
    """
    fa, fb = frame[frame[group] == a], frame[frame[group] == b]
    pa, pb = fa[metric].mean(), fb[metric].mean()
    if clustered:
        se = math.sqrt(clustered_se(fa, unit, metric) ** 2
                       + clustered_se(fb, unit, metric) ** 2)
    else:
        se = math.sqrt(naive_se(pa, len(fa)) ** 2 + naive_se(pb, len(fb)) ** 2)
    d = pb - pa
    return {"n_a": len(fa), "n_b": len(fb), "ctr_a": pa, "ctr_b": pb,
            "abs_diff": d, "rel_lift": d / pa if pa else float("nan"),
            "se": se, "z": d / se if se else float("nan"),
            "p": two_sided_p(d / se) if se else float("nan"),
            "abs_lo": d - z * se, "abs_hi": d + z * se,
            "rel_lo": (d - z * se) / pa if pa else float("nan"),
            "rel_hi": (d + z * se) / pa if pa else float("nan")}


if __name__ == "__main__":
    df = load()
    r = compare(df)
    print(f"{len(df):,} sessions   {df.user_id.nunique():,} users")
    print(f"A {r['ctr_a']:.4%}   B {r['ctr_b']:.4%}   rel {r['rel_lift']:+.2%}   "
          f"z {r['z']:.2f}   95% CI [{r['rel_lo']:+.2%}, {r['rel_hi']:+.2%}]")
