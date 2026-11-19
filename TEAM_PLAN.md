# Team plan

How four people can split the remaining work: the formal slides, further research, the talk and the Q&A. Each person owns one continuous part of the story, together with the notebook sections behind it.

Speaking times assume a talk of about 15 minutes. Scale them to the actual time limit.

## Who owns what

| Role | Slides | Notebook sections | Speaking time |
|---|---|---|---|
| **A. Story and integration** | cover, question, naive, strata, summary, advice | 1 to 4.1, 15 | about 3.5 min (opening and close) |
| **B. Identification** | selection, meanrev, traps, graph, backdoor, design | 4.2 to 6, Appendix A | about 4 min |
| **C. Estimation and robustness** | lines, result, event, toolkit, cate, robust, overlap | 7, 8, 11.3, 12 | about 4 min |
| **D. Mechanism and experiment design** | funnel, habit, share, wrong, power, holdout, iv, gformula | 9, 10, 11.1 to 11.2, 13, 14, Appendices B and C | about 4 min |

Slide names are the file names in `deliverables/slides/slides/`. The remaining appendix slides (method, bayesnet, coursemap) go with A, B and A respectively.

## A. Story and integration

- Set the template and visual style of the formal slides, and decide which slides stay in the main talk and which move to the appendix.
- Check every number on every slide against `outputs/results.json`.
- Run two full rehearsals with a timer.
- Q&A: what the retailer should do differently, and what the project does not show.

## B. Identification

Further research:

- Draw a finer causal graph, with the pre-campaign windows as separate nodes, and rerun the DoWhy graph test. The simple one-window graph is rejected.
- Add a sensitivity analysis for unobserved confounding: how strong would a hidden confounder have to be to overturn the conclusion?

Q&A:

- Why not difference-in-differences? The course does not cover it, and a plain change-from-baseline comparison gives −3.4% because the selected households are at a high point (regression to the mean).
- Why is the backdoor adjustment credible here? The retailer selects on shopping history about four months ahead, and that history is observed.
- Spending in the check window still predicts who gets a campaign. Adjusting for it as well gives −0.9% [−7.6%, +7.5%].

## C. Estimation and robustness

Further research:

- Rerun the machine-learning estimators with other random seeds and hyperparameters and report how much the estimates move.
- Trim extreme propensity scores, then rerun weighting and matching, and see whether they pass the placebo test.
- Build a separate Python 3.11 environment and try CausalML (uplift trees). It does not install on Python 3.13.
- Redraw the toolkit figure and the causal graph with larger text for the formal slides.

Q&A:

- A null result is not proof of no effect. This data can only detect a lift of about 14% or more; the interval runs from −7.6% to +11.3%.
- Why does propensity-score weighting fail? Overlap is thin: the weighted controls count for about 190 households, and the method misses the placebo by about $8.
- Why trust the nine "clean" methods? Each one finds an effect within $1 of zero in the 8 weeks before the campaign, where the true effect is zero.

## D. Mechanism and experiment design

Further research:

- Split the effect by product category and look for a category that responds.
- Work out the economics: discount cost against the incremental margin the interval allows.
- Deal with the pre-trend in the TypeB/C share analysis, or drop that analysis.

Q&A:

- Why is "customers who used a coupon spent more" a mistake? Redemption is a collider: households that shop more in a given week both redeem more and spend more.
- How large would the experiment have to be? About 72,000 households per group for a 1% lift, or about 58,000 with blocking and ANCOVA; a 2% lift with a 10% holdout needs about 81,000 in total.
- The instrumental-variable and g-formula results are illustrations. Their intervals are very wide.

## Suggested cut for a 15-minute talk

Keep about 18 slides in the main talk:

- Move `traps`, `event`, `share` and `cate` to the appendix.
- Merge `power` and `holdout` into one slide.

## Stages

1. Everyone reads their notebook sections until they can explain them without notes.
2. Further research is done in parallel. Results go into the notebook first; A decides what reaches the slides.
3. Freeze the numbers, then build the formal slides.
4. Two rehearsals. The second one includes a mock Q&A.

## Working rules

- The notebook is the source of truth. Change the analysis there, rerun it, then rebuild the report (`report/build_report.py`) and update the slides.
- Everything in the repository is written in English.
- The raw data stays out of git.
