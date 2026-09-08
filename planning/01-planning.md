# Step 1 — Planning

**Test:** Homepage dek (summary subtitle) vs. no dek
**Owner:** PM, Homepage & Discovery
**Company context:** see [00-company-brief.md](00-company-brief.md)
**Status:** Step 1 complete

---

## Goal

Increase homepage→article click-through rate to hit Q4 KR1: **+5% relative by Dec 31, 2026.**

CTR only. Articles-read-per-session (KR2) is explicitly **out of scope as a goal**, though tracked as a secondary metric. Accepted trade-off: if a variant lifts CTR but readers bounce on arrival, the primary KPI will not catch it — secondary metrics carry that load.

**Timebox:** clean testing window **Sept 22 → Oct 30, 2026.** Bounded by the thumbnail test ending Sept 22 and the Nov 3 election rendering homepage behavior unrepresentative.

---

## Primary KPI

**Session-denominated CTR** — share of homepage sessions with at least one article click.

- **Baseline: 34.1%** (38.4% twelve months ago)
- **Ship threshold: +5% relative** → 34.1% → 35.8% (+1.7pp)

### Secondary metrics

| Metric | Baseline | Why |
|---|---|---|
| Scroll depth | — | Did the dek send better-qualified readers? |
| Time on page | — | Same |
| Bounce rate | — | Primary detector of the satisfaction risk. Definition is legacy/messy — directional only. |
| Articles read per session | 1.42 | KR2 watch |
| Ad impressions per session | 3.8 | Vertical-space cost. **Not instrumented — excluded from this exercise.** |
| Dek coverage rate | TBD (dry week) | Denominator on the result's credibility |

### Pre-registered segments (exploratory only)

Device (mobile / desktop), logged-in vs. anonymous, subscriber vs. non-subscriber, new vs. returning, section.

These are **hypothesis-generating, not confirming.** Multiple comparisons across five cuts guarantees a spurious "win" somewhere. No rollout decision may be made on a segment result — it can only justify a follow-up test. *(Named explicitly because a mobile-only dek is an attractive follow-up if spacing hurts mobile — that idea must come from a dedicated test, not from this test's subgroup.)*

---

## Unit of randomization / analysis

- **Randomization: user.** Prism assigns sticky by `user_id` (logged-in) or first-party cookie (anonymous).
- **Analysis: user.** The unit of analysis cannot be finer than the unit of randomization — sticky assignment makes one user's sessions correlated, not independent.
- **Consequence:** the CXL calculator assumes independent binomial units and understates the required sample. A clustering buffer is applied (design effect ≈ 1.24, from ~1.8 homepage sessions per user over three weeks).

---

## Hypothesis

> **If** we add a one-to-two-sentence factual summary (dek) beneath homepage headlines,
> **then** the share of homepage sessions with at least one article click will increase,
> **because** readers currently skip stories they cannot evaluate from the headline alone — the top complaint in the Aug 2026 reader survey (*"I can't tell what the story is from the homepage"*) — and a dek lets them judge relevance before committing a click.

**Primary mechanism: reduction of relevance-uncertainty. Not curiosity.** This distinction is load-bearing. A curiosity-gap mechanism implies withholding, which is what the Tallow Bridge headline did and what Headline Standards Policy §2 now forbids. A dek does the opposite — it adds information.

**Secondary mechanism, declared up front:** because the dek conveys scope without necessarily stating the story's conclusion (dek rule 4 below), it also preserves a reason to click. This is named here so that it cannot later look like the theory was revised after seeing results.

### Why this test rather than the scenario's neutral-vs-emotional wording test

The Aug 2026 survey does not support the wording premise. No respondent said headlines were too boring. The top two complaints were legibility and undifferentiated presentation. Testing wording would mean testing a hypothesis the available qualitative evidence contradicts.

---

## Variants

**Single variable: presence of the dek. Headline wording is identical across arms.**

| Arm | Presentation |
|---|---|
| **A — control** | Current production homepage, untouched. Headline only. True control. |
| **B — treatment** | Identical headline + factual dek rendered beneath it. |

### Scope: slots 1–5

| Slot group | Per-impression CTR | ~Share of homepage clicks | Deks live at once |
|---|---|---|---|
| Slot 1 | 9.1% | ~26% | 1 |
| **Slots 2–5** | **4.3%** | **~43%** | 4 |
| Slots 6–20 | 1.9% | ~27% | 15 |
| Slots 21–48 | 0.8% | ~4% | 28 |

**Slots 1–5 cover ~69% of all homepage clicks with five deks live at a time** — roughly seven-tenths of the target behavior for a tenth of the operational cost of covering the page.

Rejected: **slot 1 only** touches ~26% of clicks and appears in ~1 impression per session, leaving almost no room to move a session-level metric — a true-but-invisible result. **Slots 1–20** adds 15 deks for 27% more clicks (worse cost-per-click-covered). **All 48** is a redesign, not a test.

### Dek sourcing: reporter drafts, homepage desk holds final edit

Reporter writes the dek at filing time — they know the story, know the punchline, and building it into the filing workflow means coverage is structural rather than bolted on. The field remains valuable for future tests even if this one loses. The homepage desk may override at curation time for the five in-scope slots, which bounds quality variance across ~140 filers.

**Workload note:** user-level randomization means the dek is written **once per story, not twice.** Editorial writes one dek; Prism shows it to 50% of readers and hides it from the other 50%. The ask is "+1 dek per in-scope story," not "double the headline work."

### Dek standard

> 1. Maximum two sentences.
> 2. Independently accurate. Same standard as the headline.
> 3. Topically continuous with the headline. It may add context, stakes or scope; it may not introduce a different subject, and it may not contradict or reframe the headline. *(Prevents "headline says one thing, dek says another" trust damage.)*
> 4. It must convey **what the story covers** — the scope of what a reader will find. It is **not required** to state the story's conclusion or resolution.
> 5. It must not gesture at withheld information. No "what happened next," no "the reason may surprise you," no unnamed subjects.
> 6. **Operative test:** a reader who reads only the dek should be able to say what the story is about and decide whether it is for them. They should not feel a question has been deliberately dangled in front of them.

Rule 4 preserves a reason to click. Rule 5 is what keeps the variant inside Headline Standards Policy §2 — it passes because the *headline* still fully names its subject — nothing is hidden to compel the click; the reader knows what the story is about and is choosing whether to read the detail.

### Handling stories with no dek

**All stories always appear on the homepage in both arms.** No story is withheld or excluded from the surface — that would give arms A and B different story sets, which would test curation, not deks.

Log two separate flags:

| Flag | Logged in | Determined by | Safe to filter on? |
|---|---|---|---|
| `dek_available` — a dek exists for the story | **Both arms** | Reporter/desk — independent of arm assignment | **Yes** |
| `dek_rendered` — the dek was displayed | Arm B only, by definition | Treatment assignment | **Never** |

`dek_available` is treatment-independent: whether a reporter wrote a dek has nothing to do with which bucket a reader landed in. It can therefore be conditioned on **symmetrically in both arms** without breaking comparability. In arm A, `dek_available=true, dek_rendered=false` is a real and useful state.

`dek_rendered` is *caused by* treatment. Filtering on it would remove sessions from arm B only — comparing a filtered treatment group to an unfiltered control group, which destroys randomization and invalidates the p-value. Log it for QA; never for analysis.

### Analysis plan

- **Primary — intention-to-treat.** Every assigned user, every session, no filtering. Unbiased. This is the reported number. It **understates** the true dek effect in proportion to coverage gaps; that is the honest price of an unbiased estimate.
- **Secondary, pre-registered — availability-conditioned.** Sessions where all five in-scope slots had `dek_available=true`, compared across both arms. Estimates the effect of a dek when a dek exists. Supporting evidence only: availability likely correlates with story type (wire copy and breaking news are the likeliest gaps, and those sessions behave differently).
- **Always reported:** dek coverage rate over the window.

---

## Randomization strategy

| | |
|---|---|
| Unit | User (sticky) |
| Split | **50/50** — maximizes power; no reason to hold back |
| Eligibility | **All homepage traffic.** No device, login-state, geo or section restriction — the result needs to generalize, and segment cuts are how the mobile/desktop question gets asked. |
| Mechanism | Prism sticky assignment: `user_id` for logged-in, first-party cookie for anonymous |
| Allocation granularity | 5% increments (platform constraint) — 50/50 is fine |
| Concurrency | Max 4 homepage tests; the thumbnail test frees a slot Sept 22 |
| Known leakage | ~12%/month anonymous cookie churn; ~7% of anonymous users cross devices within a 2-week window. Both dilute toward the null — they cost sensitivity, not validity. |

---

## Sample size estimate

Via [cxl.com/ab-test-calculator](https://cxl.com/ab-test-calculator/) — 95% confidence, 80% power, 34.1% control conversion rate, 1 variant, **relative** MDE, two-sided test, 1,525,000 weekly homepage users.

| MDE (relative) | Absolute | Calculator: per group | **+1.24 clustering buffer** | Total |
|---|---|---|---|---|
| **+2% — power target** | 34.1% → 34.8% | 75,950 | **~94,200** | **~188,400** |
| +5% — ship threshold | 34.1% → 35.8% | 12,177 | ~15,100 | ~30,200 |

### The key finding: sample size is not the binding constraint — the runtime floor is

188,400 users is about **12% of a single week's homepage traffic.** The test is fully powered inside 24 hours and then runs for three more weeks **for validity, not for power.**

### Why power for +2% while shipping at +5%

Two different concepts that the word "MDE" tends to collapse:

- **Power target (+2% relative)** — the smallest effect the test can reliably *detect*. Nearly free at this traffic volume.
- **Ship threshold (+5% relative)** — the business bar for rolling out a newsroom workflow change.

---

## Stopping conditions

### Minimum runtime: 3 weeks, one efficacy decision

| Date | Event |
|---|---|
| **Sept 15–21** | **Dry measurement week.** Reporters begin filing deks; nothing renders on the homepage. Measures coverage only. This week *is* the newsroom rollout. |
| **Sept 22** | Launch (thumbnail test ends) |
| **Oct 13 (day 21)** | **Health check — no efficacy decision.** Guardrails, dek coverage, SRM, rendering, observed design effect vs. the 1.24 assumption, week-over-week effect drift. |
| **Oct 27 (day 35)** | **Single efficacy analysis, α = 0.05** |
| Oct 30 | Hard stop — window closes before election distortion |

Three weeks minimum covers multiple full weekly cycles, so weekday/weekend reader-mix differences average out rather than driving the result.

### Launch gate: dek coverage ≥ 85%

ITT dilution makes coverage a **go/no-go condition, not a footnote.** At 60% coverage, the ITT estimate shrinks by ~40% — a true +3% lift arrives as +1.8%. Measure coverage of slot 1–5 story-hours during the dry week; require **≥85%** before launching. If it comes in low, fix the workflow rather than burning the only clean pre-election window on a diluted test.

### Guardrails

| Guardrail | Trip condition | Rationale |
|---|---|---|
| **Primary KPI harm** | Observed relative CTR ≤ −5% **and** significant at 95%, on or after **day 5**. Hard override: ≤ −10% relative at any point after day 2. | Day-1 noise is enormous; the day-5 floor prevents killing a sound test on Tuesday jitter. The override exists so a genuine disaster does not wait five days. |
| **Subscriber churn (rise)** | **Two layers.** (1) Daily tripwire: treatment-arm cancellations ≥1.5× control for 2 consecutive days, or ≥2× on any single day. (2) Non-inferiority test at Oct 13 and Oct 27 against a **+10% relative harm margin** — pass only if the 95% CI upper bound sits below the margin, regardless of p-value. Detectable effect ~10% relative at 3 weeks, ~7% at 5 weeks. Compared arm-to-arm, never to history. Permitted at both dates because guardrails are asymmetric — they can stop the test, never declare a win. | Churn is the documented failure mode for headline changes here. Churn lags exposure (renewal-date cancellations), so cohort tracking continues 60–90 days post-test. |
| **Bounce rate** | Treatment ≥ control +3pp, significant at 95%, on or after day 5 | The satisfaction risk surfacing. Bounce definition is legacy/messy — a trip means *investigate*, not auto-kill. |
| **Standards escalation** | Any formal editorial-standards escalation | Non-negotiable, non-statistical. KR3. |

**Deliberately excluded: ad impressions per session.** Prism auto-alerts only on bounce rate, session length and cancellations; ad impressions per session is not wired in and would need a named owner performing a manual daily pull. **Out of scope for this exercise** — the vertical-space risk to ad inventory is real and is recorded in the risk table as knowingly unmonitored. In a live version of this test it should be instrumented before launch, and it would be well powered: at ~3.8 ad impressions per session across ~305,000 daily sessions, event volume dwarfs the churn guardrail's.

### Peeking policy

1. **Pre-register before launch.** Hypothesis, KPI, MDE, confidence/power, guardrails and thresholds, minimum runtime, analysis dates, segment list — written down and signed off before a single user is assigned.
2. **Anyone may look. Only Oct 27 may decide the outcome.** Oct 13 is a health check, not a decision point.
3. **Guardrail monitoring is daily and exempt.**
4. **One efficacy analysis, at the full α = 0.05 — Oct 27.**
5. **Weekly status summary** reports observed lift with confidence intervals, labelled *"not yet at a decision point"* — a fixed reporting cadence removes the reason to go looking for one.

#### Why one look, not two

O'Brien-Fleming assumes information accrues across the test, making an interim genuinely early and an early stop a saving of sample. This test is fully powered for +2% relative **within 24 hours**. Nothing is scarce at the interim, there is no sample to save, and stopping early would defeat the entire purpose of the three-week floor, which exists for **validity** (weekly cycles, novelty decay) rather than power.

So: **Oct 13 is a health check with no efficacy claim available at any p-value, and Oct 27 is a single efficacy analysis at the full α = 0.05.** More power, a simpler pre-registration, and — the operative benefit — **no legitimate path to an early call.**

---

## Assumptions

| # | Assumption | If it fails |
|---|---|---|
| 1 | **Instrumentation is sound** — Prism assignment is correct, no sample ratio mismatch, session-CTR logging is accurate, and `dek_available` fires on every in-scope impression in **both** arms | The whole result is void. Verify with an A/A sanity check and an SRM check on day 1. |
| 2 | **No competing homepage change ships during the window** — no redesign, no CMS change, no fourth concurrent test in slots 1–5 | Confounded result, unattributable |
| 3 | **Dek coverage ≥85% of slot 1–5 story-hours** | ITT dilution; underpowered in practice despite the paper calculation. Gated by the dry week. |
| 4 | **Dek quality is roughly consistent** across ~140 filers — reporter draft plus desk edit bounds the variance | Measures "average dek quality," not "the dek concept." A null could mean bad deks rather than a bad idea. |
| 5 | **Curation behavior is unchanged** — the homepage desk does not begin selecting different stories because deks now exist | Testing curation, not deks. Highest-risk unmeasured confound, because curation is human. Worth a pre/post check on story-mix composition. |
| 6 | **Assignment leakage stays small** — 12%/mo cookie churn and 7% cross-device dilute but do not dominate over 3–5 weeks | Diluted effect; biases toward the null, so a win remains trustworthy while a null becomes ambiguous |
| 7 | **No exogenous news shock** dominates behavior inside the window | Noise swamps a 2% effect. Pre-election period makes this non-trivial. |
| 8 | **Novelty decays inside the window** — three weeks is enough for behavior to stabilize | An early lift that fades. Mitigate by comparing week 1 vs. week 3 effect size. |
| 9 | **Rendering is consistent** — the dek displays as designed across devices, browsers and viewport sizes | Mobile users may get a broken or truncated treatment. QA before launch, not after. |
| 10 | **Session-CTR is a valid proxy** for the engagement the business actually wants | A win on paper, no business value. This is precisely why KR2 and the secondary metrics stay instrumented despite being out of scope as goals. |
| 11 | **The design effect ≈1.24 is approximately right** — ~1.8 homepage sessions per user over three weeks | Under-powered relative to plan. Recompute from live data in week 1 and adjust the final analysis date if needed. |

---

## Risks

| Risk | Detail | Mitigation |
|---|---|---|
| **Satisfaction risk** *(most likely loss mode)* | A good summary answers the reader's question and removes the reason to click. Exactly the dynamic that cost Meridian its search traffic to AI answer engines. | Dek rule 4 (scope, not conclusion). Bounce-rate guardrail. **Predict this publicly before launch** — it converts a loss into a validated learning rather than a miss. |
| **Vertical space → fewer impressions** | Deks push stories down; fewer headlines above the fold, fewer impressions per session. | Session-denominated KPI partly insulates the primary metric. Tracked via impressions/session and ad impressions/session. |
| **Ad revenue** *(accepted, unmonitored)* | Fewer above-fold slots means less ad inventory per session. Baseline 3.8 ad impressions/session. | **None — knowingly accepted for this exercise.** Not instrumented, excluded from the guardrail set. In a live test it would be guardrailed at −5% sustained 3 days. |
| **Opposing metric movement** | CTR up **and** ad impressions per session down is a plausible joint outcome — the test can win on its primary while losing on inventory. | Decide the tiebreak rule **before** the readout, not after seeing it. Not a statistical question; no analysis resolves it. |
| **Curation confound** | Human curation could shift in response to deks existing (assumption 5). | Pre/post story-mix composition check. Brief the desk that selection behavior should not change. |
| **Timeline** *(most likely cause of slippage)* | Changing how ~140 people file, plus a CMS field, plus training, plus standards sign-off — in 14 days, during a pre-election news cycle. | The dry week is the rollout week and produces a coverage number instead of a hope. If coverage <85%, slip rather than launch diluted. |
| **Editorial workload** | Slot 1 turns over 8–14× daily, so dek production must keep pace during breaking news. | Scope limited to 5 slots; one dek per story; reporter drafts so the desk only edits. |
| **Novelty effect** | Early lift from unfamiliarity rather than utility. | Three-week minimum; compare week 1 vs. week 3 effect size. |
| **Election proximity** | Oct 30 hard stop leaves only ~3 days of buffer before Nov 3 distortion begins. | Hard stop is non-negotiable. Any need to extend means re-running after Nov 15, when mobile viewability also ships. |