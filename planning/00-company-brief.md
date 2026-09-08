# The Meridian — Company Brief

> Fictional company created for an A/B testing exercise. All figures are invented.
> Scenario: Online media — optimizing headline CTR.

---

## The business

Digital-first national news publisher, US-based, founded 2009 as a blog network, now a mid-tier general-news outlet. No print. Positioned between the legacy nationals and the aggregators: serious reporting, faster metabolism, "explains the news without shouting."

| | |
|---|---|
| Monthly unique visitors | 14.2M |
| Monthly sessions | 41M |
| Revenue mix | 61% programmatic + direct ads, 34% subscriptions, 5% licensing/events |
| Paying subscribers | 218,000 ($9/mo standard) |
| Voluntary subscriber churn | ~2.8%/mo (~6,100/mo, ~200/day) |
| Newsroom | 140 editorial staff |
| Articles published | ~90/day |
| Business status | Roughly break-even. Two rounds of layoffs since 2024. Board wants subscriptions at 40% of revenue by end of 2027. |

---

## Traffic & the homepage

The homepage is Meridian's most valuable owned surface — where subscribers and habitual readers land, and it converts far better than search or social traffic.

| Metric | Current | 12 months ago |
|---|---|---|
| Homepage sessions/day | ~305,000 | ~340,000 |
| Share of all sessions entering via homepage | 22% | 19% |
| **Sessions with >=1 article click** | **34.1%** | 38.4% |
| Avg. headline impressions per homepage session | 11.4 | — |
| Per-impression CTR (all slots, blended) | 3.2% | 3.7% |
| Device mix (homepage) | 68% mobile, 29% desktop, 3% tablet | — |
| Logged-in share of homepage sessions | 31% | — |
| Articles read per session | 1.42 | — |
| Ad impressions per homepage session | 3.8 | — |

### Homepage layout

6 curated modules, 48 article slots total. CTR varies enormously by slot:

| Slot group | Per-impression CTR |
|---|---|
| Slot 1 (lead) | 9.1% |
| Slots 2–5 (above fold) | 4.3% |
| Slots 6–20 | 1.9% |
| Slots 21–48 | 0.8% |

Approximate share of all homepage article clicks by slot group: slot 1 ~26%, slots 2–5 ~43%, slots 6–20 ~27%, slots 21–48 ~4%. **Slots 1–5 account for roughly 69% of homepage clicks.**

Curation is human. A rotating homepage desk (3 editors per shift, 3 shifts) chooses and orders stories. Slot 1 turns over 8–14 times a day.

### Why CTR is falling — three competing internal theories, none proven

1. Search referral collapse from AI answer engines changed the visitor mix (more habitual, fewer casual).
2. The March 2026 homepage redesign pushed more stories above the fold — more impressions, thinner attention per headline.
3. Headlines have gotten "flatter" since the Tallow Bridge incident.

---

## The Tallow Bridge incident (March 2026)

A homepage headline read: *"The one detail about the Tallow Bridge collapse nobody is talking about."* It drove 4.1x normal slot-1 CTR. It was also accurate but withholding — the "detail" was a routine inspection lapse already in paragraph two.

It was quote-tweeted into the ground by other journalists. Meridian's own reporters publicly distanced themselves. Over the following nine days: **412 subscription cancellations**, ~180 citing the headline in their exit survey, and a Poynter piece naming Meridian.

Consequences that still bind:

- A written **Headline Standards Policy**, enforced by a new Standards & Ethics Editor role.
- The Editor-in-Chief holds **veto power over any homepage experiment touching headline language**.
- Internally, "curiosity gap" is a loaded phrase. Say "engagement-forward" if you want people in the room.

---

## Headline Standards Policy (excerpt, v2.1)

1. A headline must be independently accurate — true on its own, without the article as a crutch.
2. A headline must not withhold its own subject in order to compel a click.
3. Emotional language is permitted where the emotion is the story's own, not manufactured.
4. No second-person address ("You won't believe…"). No numbered-list framing for news reporting.
5. Superlatives require sourcing.
6. Standards Editor review is required for any headline template applied at scale.

**What the policy does NOT forbid:** emotional register, stakes-forward framing, human-subject framing, present tense, curiosity that names its subject. There is real room here — narrower than "clickbait vs. neutral," wider than "wire-service dry."

---

## Your role

**Product Manager, Homepage & Discovery.** Fourteen months in. You own the homepage surface, the recommendation modules, and the discovery experiment roadmap.

- **You own:** experiment design, prioritization on the homepage surface, the discovery roadmap, calling tests to a stop.
- **You don't own:** headline copy (Editorial), the paywall (Subscriptions), ad slot inventory (Revenue).
- **You need sign-off from:** Editorial for anything altering published headline text; Standards for anything applied as a repeatable template.

---

## Stakeholders

| Person | Role | What they want | What makes them say no |
|---|---|---|---|
| **Halvard Osei** | Editor-in-Chief | Newsroom credibility, no repeat of March. Genuinely open to data, has been burned. | Anything that reads as testing readers' gullibility, or that puts the newsroom's byline behind copy an algorithm chose. Wants to know who wrote the variant. |
| **Junko Reyes** | Standards & Ethics Editor | A defensible, documented rule for what's allowed. New in role, needs to demonstrate teeth. | Vague variant definitions. Will ask "show me ten example headlines" before approving anything. |
| **Tomasz Delgado** | VP Audience Growth | Q4 engagement OKR. Closest ally, also biggest pressure source. | Slow tests. Tests with an MDE so small the result won't move his number. Will push to call it early. |
| **Nneka Brandt** | Director of Ad Revenue | Page views and ad impressions per session. Cares about the test only if it moves inventory. | Anything that risks Q4 inventory during election season. |
| **Yusuf Kalvøy** | Staff Data Scientist (shared, ~30% allocated to you) | Methodological soundness, his own credibility. | Peeking, no pre-registration, undefined units of analysis. Will write a memo if you get it wrong. |
| **Marguerite Oyelaran** | Homepage Desk Lead | Not having her shift's workflow disrupted. Her desk produces whatever variants you design. | Anything doubling headline-writing workload during breaking news. |
| **Ines Tarkovsky** | Director of Product, Discovery — your manager | A win she can present at Q4 review. Will back you if the design is clean. | Being surprised in a stakeholder meeting. |

---

## Q4 2026 OKRs (yours)

- **KR1:** Increase homepage→article click-through rate by 5% relative by Dec 31, 2026.
- **KR2:** Increase articles-read-per-session from 1.42 to 1.55.
- **KR3:** Zero standards escalations from homepage experiments.

KR3 is not decorative. Osei added it.

---

## Experimentation capability

Platform: **Prism**, in-house, built 2023. Mature enough to trust, quirky enough to plan around.

- **Assignment:** sticky by `user_id` (logged-in) or first-party cookie (anonymous). Anonymous cookie churn ~12%/month; ~7% of anonymous users cross devices in a 2-week window.
- Supports headline-level variant rendering at the slot level. Variants authored in the CMS as alternate headline fields.
- Traffic allocation configurable in **5% increments**. Max **4 concurrent homepage experiments** (interaction-effect guardrail).
- Results dashboard updates hourly. **Shows raw p-values with no sequential correction** — Kalvøy calls this "the loaded gun."
- Automated guardrail alerting for bounce rate, session length, subscription-cancellation rate. **No automated stop** — alerts page you.

### Instrumentation reality

- Headline impressions logged for all slots. **Viewability (was it actually on screen?) is only tracked on desktop.** Mobile viewability ships Nov 15, 2026 — so impression-denominated CTR is only clean for 29% of traffic today.
- Scroll depth and time on page: reliable on article pages.
- Bounce rate definition is legacy and messy — single-page-session based, doesn't account for read time.

### Currently running on the homepage

One test — thumbnail aspect ratio, slots 6–20, ends **Sept 22**. Overlaps anything started now.

---

## Calendar

| Date | Event |
|---|---|
| Sept 22 | Thumbnail test ends |
| Oct 1 | Q4 begins |
| **Nov 3** | **National midterm elections — expect 3–5x traffic, atypical reader behavior, homepage in live-blog mode for ~72h** |
| Nov 15 | Mobile viewability instrumentation ships |
| Dec 3 | Q4 review — Tarkovsky presents |
| Dec 20 – Jan 2 | Holiday traffic trough, ~40% below baseline |

---

## Prior work

- **June 2026 — Slot-1 image vs. no image.** Won, +6.2% relative CTR. Shipped. Established that Prism works and that Osei will accept a well-run homepage test.
- **Feb 2026 — Headline length (short vs. long).** **Inconclusive.** Ran 4 days, underpowered, killed when Tallow Bridge blew up. Nobody trusts the result. This is the test yours will be compared to.
- **Aug 2026 — Qualitative reader survey (n=340).** Top complaint about Meridian: *"I can't tell what the story is from the homepage."* Second: *"too many stories, all the same size."* **Nobody said headlines were too boring.**

That last finding cuts against the premise of the test. Worth addressing in the hypothesis.

---

## The scenario as given

**Context**
- Headlines strongly influence clicks
- Editors care about tone
- Marketing wants engagement, without clickbait
- Traffic is high enough for rapid experimentation

**Possible variants**
- A: Neutral, factual headline
- B: Emotional or curiosity-driven headline

**Primary KPI:** CTR (homepage → article)
**Secondary metrics:** Scroll depth, time on page, bounce rate
