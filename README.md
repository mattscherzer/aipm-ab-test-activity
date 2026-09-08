# A/B Test Activity — Homepage Summary Test

A worked A/B testing exercise taken end to end: plan the test, generate synthetic data, analyse it,
decide, present it. The scenario is a fictional digital news publisher optimising homepage headline
click-through.

**The presentation is the entry point:** [`index.html`](index.html) — three slides, keyboard-driven.

---

## Layout

```
index.html               the deck — also what GitHub Pages serves
presentation-script.md   the speaking script, kept out of the deck on purpose
planning/                the written work
  00-company-brief.md
  01-planning.md
analysis/                the computational work
  02-synthetic-data.ipynb
  03-results.ipynb
  04-early-peeking.ipynb
  abtest.py
  ctr_by_variant.png
  ab_test_sessions.csv   (generated, not committed)
```

| File | What it is |
|---|---|
| [`index.html`](index.html) | **The deck.** Three slides. Carries no speaker notes by design — it is meant to be screen-shared. `P` prints it. |
| [`presentation-script.md`](presentation-script.md) | The script — a setup beat, then per-slide notes with timings and stage directions, plus a numbers cheat-sheet and likely questions. Read it on a second device. |
| [`planning/00-company-brief.md`](planning/00-company-brief.md) | The fictional company. Traffic, baselines, platform constraints, calendar. |
| [`planning/01-planning.md`](planning/01-planning.md) | **Step 1** — goal, KPI, hypothesis, variants, randomisation, sample size, stopping conditions, assumptions, risks. |
| [`analysis/02-synthetic-data.ipynb`](analysis/02-synthetic-data.ipynb) | **Step 2** — generates the dataset and verifies it matches spec. The single source for the data. |
| [`analysis/03-results.ipynb`](analysis/03-results.ipynb) | **Step 3** — validity gates, conversion per variant, uplift, significance, ITT dilution, guardrails, robustness, segments, the decision. |
| [`analysis/04-early-peeking.ipynb`](analysis/04-early-peeking.ipynb) | **Step 4** — cumulative conversion by variant, the winner flipping, an A/A simulation of peeking, and what stopping early would have cost. |
| [`analysis/abtest.py`](analysis/abtest.py) | Shared helpers: the plan constants and the clustered-variance formula, defined once so the notebooks cannot drift apart. |
| `analysis/ctr_by_variant.png` | The headline chart. Written by notebook 03. |
| `analysis/ab_test_sessions.csv` | The dataset — 150,568 sessions, 100,000 readers. Generated, not committed. |

---

## Setup

Requires [uv](https://docs.astral.sh/uv/). Nothing else — uv fetches its own Python.

```bash
uv sync
```

That reads `pyproject.toml`, resolves against the committed `uv.lock`, and builds `.venv`. Same
versions on every machine.

## Run

```bash
uv run jupyter lab
```

Open `analysis/02-synthetic-data.ipynb` first (it writes the dataset), then `03` and `04`. Pick the
**Python 3 (uv)** kernel. All three ship with outputs rendered, so they can also just be read.

`analysis/ab_test_sessions.csv` is not committed — it is 11 MB and byte-reproducible from the seed.
To build it without opening Jupyter:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace analysis/02-synthetic-data.ipynb
```

## GitHub Pages

Pages serves **`index.html` from the repository root**. When that file does not exist, Jekyll falls
back to rendering `README.md` as the index — which is why an earlier push showed this file instead of
the deck. The deck is now `index.html`, so a push to the Pages branch serves it directly with no
configuration.

`.nojekyll` sits alongside it to stop Jekyll from processing the site at all. The deck is plain HTML
with no build step, so there is nothing for Jekyll to do except potentially get in the way.

The one external dependency is Google Fonts (Newsreader and Libre Franklin). Both have real fallback
stacks, so the deck degrades to Georgia and a system sans if the network blocks them.

---

## Reproducibility

Everything flows from `SEED = 20260922`, with fixed offsets per stage: `SEED` for the day structure,
`SEED + 10` for readers, `SEED + 2` inside calibration, `SEED + 11` for the write. Re-running produces
a **byte-identical** CSV.

The write cell in notebook 02 carries two guards:

- **`REGENERATE = False`** uses the CSV on disk instead of rewriting it — set this once you are
  analysing rather than generating, so a top-to-bottom re-run cannot clobber your data.
- **A SHA-256 check** against the exact dataset the analysis notebooks report on. Changing any config
  value in cell 1 is legitimate, but the checksum will then mismatch and say so loudly, because every
  number downstream belongs to the old dataset.

## Dataset spec compliance

| Requirement | Result |
|---|---|
| Medium-to-large sample | 150,568 sessions / 100,000 readers |
| Slightly uneven split | Intended 52/48, realised 52.03/47.97 |
| 10–30% uplift for best variant | +11.90% relative |
| Realistic variance and noise | Reader random effects, weekly cycle, day-level news noise, one shock day, covariate effects, coverage gaps, novelty decay |
| Integrity | 0 failures across 8 structural invariants |
| SRM vs intended allocation | z = −0.73, p = 0.463 — pass |
| Design effect from clustering | 1.231 measured, 1.24 planned |

## Headline result

| | |
|---|---|
| Variant A — headline only | 34.01% session CTR (78,341 sessions) |
| Variant B — headline + summary | 38.06% session CTR (72,227 sessions) |
| Uplift | +4.05pp, **+11.90% relative** |
| 95% CI (reader-clustered) | +10.32% to +13.49% |
| Recommendation | **Roll out**, conditional on instrumenting ad inventory and verifying churn |

Caveat worth carrying: the +12% effect exists because the brief asked for 10–30%. A real summary
would not move session CTR by twelve percent, so every judgement call in notebook 03 is easy. Setting
`TARGET_B = 0.351` in notebook 02 gives a realistic +3% version, where the clustering correction and
the ITT dilution would actually decide the outcome.
