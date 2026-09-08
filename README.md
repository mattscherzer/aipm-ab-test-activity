# A/B Test Activity — Meridian Homepage Dek Experiment

A worked A/B testing exercise: plan the test, generate synthetic data, analyse it, decide.
Scenario is a fictional digital news publisher optimising homepage headline CTR.

## Setup

Requires [uv](https://docs.astral.sh/uv/). Nothing else — uv fetches its own Python.

```bash
uv sync
```

That reads `pyproject.toml`, resolves against the committed `uv.lock`, and builds `.venv`.
Same versions on every machine.

## Run

**The notebooks** — Step 2 generates the data, Step 3 analyses it. Run them in order:

```bash
uv run jupyter lab
```

Pick the **Python 3 (uv)** kernel. It ships with outputs rendered, so it can also just be read.

`ab_test_sessions.csv` is not committed — it's 11 MB and byte-reproducible from the seed. Running
the notebook creates it. To build it without opening Jupyter:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace 02-synthetic-data.ipynb
uv run jupyter nbconvert --to notebook --execute --inplace 03-results.ipynb
```

Both notebooks ship with outputs rendered, so they can be read without running anything.

## Files

| File | What it is |
|---|---|
| `00-company-brief.md` | The fictional company. Traffic, baselines, platform constraints, calendar. |
| `01-step1-planning.md` | **Step 1** — goal, KPI, hypothesis, variants, randomisation, sample size, stopping conditions, assumptions, risks. |
| `02-synthetic-data.ipynb` | **Step 2** — generates the dataset and verifies it matches spec. Config, generator, column dictionary, integrity checks, generator diagnostics. The single source for the data. |
| `03-results.ipynb` | **Step 3** — the analysis. Validity gates, conversion per variant, uplift, significance, ITT dilution, guardrails, robustness, segments, the decision and follow-ups. |
| `04-early-peeking.ipynb` | **Step 4** — cumulative conversion by variant, the winner flipping, an A/A simulation of peeking, and what stopping early would have cost. |
| `presentation.html` | **Stakeholder deck** — three slides, keyboard-driven. |
| `ctr_by_variant.png` | The headline chart — CTR per variant with 95% CIs. Written by notebook 03. |
| `abtest.py` | Shared helpers: the plan constants and the clustered-variance formula, defined once so notebooks 03 and 04 cannot drift apart. |

## Reproducibility

Everything flows from `SEED = 20260922`, with fixed offsets per stage: `SEED` for the day
structure, `SEED + 10` for users, `SEED + 2` inside calibration, `SEED + 11` for the write. Re-running
produces a **byte-identical** CSV.

The write cell carries two guards:

- **`REGENERATE = False`** uses the CSV on disk instead of rewriting it — set this once you're
  analysing rather than generating, so a top-to-bottom re-run can't clobber your data.
- **A SHA-256 check** against the exact file `03-results.md` reports on. Changing any config value
  in cell 1 is legitimate, but the checksum will then mismatch and say so loudly, because every
  number in the results doc belongs to the old dataset.

## Dataset spec compliance

| Requirement | Result |
|---|---|
| Medium-to-large sample | 150,568 sessions / 100,000 users |
| Slightly uneven split | Intended 52/48, realised 52.03/47.97 |
| 10–30% uplift for best variant | +11.90% relative |
| Realistic variance and noise | User random effects, weekly cycle, day-level news noise, one shock day, covariate effects, coverage gaps, novelty decay |
| Integrity | 0 failures across 8 structural invariants |
| SRM vs intended allocation | z = −0.73, p = 0.463 — pass |
| Design effect from clustering | 1.231 measured, 1.24 planned |

## Headline result

| | |
|---|---|
| Arm A — headline only | 34.01% session CTR (78,341 sessions) |
| Arm B — headline + dek | 38.06% session CTR (72,227 sessions) |
| Uplift | +4.05pp, **+11.90% relative** |
| 95% CI (user-clustered) | +10.32% to +13.49% |
| Recommendation | **Roll out**, conditional on instrumenting ad impressions and verifying churn |

Caveat worth carrying: the +12% effect exists because the brief asked for 10–30%. A real dek would
not move session CTR by twelve percent, so every judgement call in `03-results.md` is easy. Setting
`TARGET_B = 0.351` in the notebook gives a realistic +3% version, where the clustering correction
and the ITT dilution would actually decide the outcome.
