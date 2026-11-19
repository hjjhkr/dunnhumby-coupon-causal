# Do Coupons Create Sales, or Just Give Money Away?

Final project for a Causal Modeling course. Using dunnhumby's "The Complete Journey" (2,500 households, about two years of purchases, 30 coupon campaigns), we estimate the causal effect of targeted coupon campaigns on household spending.

## What we found

1. **No detectable lift.** After a first campaign, weekly spending changes by about +1% (95% confidence interval −8% to +11%).
2. **Simple comparisons mislead in both directions.** A direct comparison says recipients spend 4.5 times as much; a plain difference-in-differences says coupons cut spending by 4–10%. Both come from how the retailer selects households.
3. **Coupons mostly subsidized existing purchases.** 73% of recipient households never redeemed, and 82% of redeemed items were in a product sub-category the household had bought in the previous six months.
4. **The data cannot detect small effects.** Detecting a 1% lift would take about 72,000 households per group in a randomized test.
5. **The course toolkit agrees.** Of 15 estimators (ANCOVA, propensity scores four ways, S/T/X-learners, double ML, doubly robust learner, causal forest), the 9 that pass a placebo test put the effect between −$0.1 and +$1.3 a week (−0.3% to +2.8%). Propensity-score weighting fails the placebo test because overlap is thin.
6. **No responsive subgroup.** Causal-forest estimates by shopping frequency run from +$0.3 to +$1.3 a week, and every interval includes zero.

## What is in this repository

| Path | Contents |
|---|---|
| `coupon_causal_analysis.ipynb` | **The core deliverable.** The whole analysis, commented step by step, with all figures and results |
| `deliverables/report.html` | Interactive web report: contents rail, causal-graph explorer, method filter, sample-size calculator (open it in a browser) |
| `deliverables/Do Coupons Create Sales - slides.pptx` | The 30-slide deck as PowerPoint (one image per slide, slide text in the speaker notes) |
| `deliverables/slides/` | Source files of the slide deck (30 slides, 7 of them appendix) |
| `report/` | Template and build script that turn the notebook's results into the web report |
| `outputs/figures/`, `outputs/tables/` | Figures and tables written by the notebook |
| `outputs/results.json` | Every number quoted in the report and the slides |
| `TEAM_PLAN.md` | How four people split the slides, further research, talk and Q&A |
| `data/raw/` | The 8 raw CSV files (not in the repository, see below) |

## Method in one paragraph

The data is observational: the retailer sent coupons to its most frequent shoppers, chosen about four months ahead. We draw the causal graph, read off the backdoor paths (pre-campaign shopping history causes both the coupon and the spending) and estimate the effect on the treated by adjusting for that history. For each cohort of households receiving a campaign for the first time, the control group is the households that had not received any campaign yet, weighted (entropy balancing) to match the treated on pre-campaign spending, trips and visit frequency; the outcome is the change from a baseline window, and the estimator is doubly robust. The last 8 weeks before each campaign are held out from the adjustment and used as a placebo test.

## How the notebook is organised

| Section | Contents | Course week |
|---|---|---|
| 1–3 | Setup, data, weekly household panel | |
| 4 | Naive comparison, the selection rule, regression to the mean, Simpson's paradox and the adjustment formula | 1, 4, 5 |
| 5 | Causal graph, chains / forks / colliders, backdoor criterion, the estimand (ATT), testing the graph with DoWhy | 4, 5, 6 |
| 6–7 | Study design and the main result with a placebo window | 5, 7 |
| 8 | Course toolkit: OLS and ANCOVA, partial correlation, VIF, propensity scores four ways, DoWhy refuters, EconML meta-learners, double ML, doubly robust learner, causal forest | 1, 3, 5, 7 |
| 9–10 | Mechanisms: redemption and the share of spending on promoted products | |
| 11 | Heterogeneity, the collider mistake ("redeemers spend more"), causal-forest CATE | 4, 7 |
| 12 | Robustness | 5 |
| 13 | Sample size, blocking, ANCOVA and a holdout design for a randomized test | 2, 3 |
| 14 | Instrumental variable (LATE) and attribution | 6, 8 |
| 15 | Conclusions and a map from course topics to notebook sections | |
| Appendix A | Bayesian network learned by hill climbing with BIC | 9 |
| Appendix B | Two campaigns over time and the g-formula | 7 |
| Appendix C | Measurement error in the pre-campaign measures (one-factor reliabilities) | 8 |

## Limitations worth knowing

- Spending in the placebo window still predicts who gets a campaign, so the main estimate may be biased slightly upward; adjusting for the placebo window as well gives −0.9% [−7.6%, +7.5%].
- DoWhy's falsification test rejects the simple one-window graph, which is why the placebo test carries the argument.
- The instrumental-variable and g-formula sections are illustrations; their intervals are very wide.
- CausalML and semopy could not be installed in this environment (Python 3.13); EconML and DoWhy cover the same methods, and a structural equation model that was tried did not fit and is not reported.

## Reproducing the results

1. Download the data from [Kaggle](https://www.kaggle.com/datasets/frtgnn/dunnhumby-the-complete-journey) or the [dunnhumby source files page](https://www.dunnhumby.com/source-files/) and put the 8 CSV files in `data/raw/`. The data's terms of use do not allow redistribution, so it is not in this repository.
2. Create an environment and install the dependencies:

   ```powershell
   python -m venv .venv
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. Open `coupon_causal_analysis.ipynb` and run all cells (about 10 minutes; most of it is the bootstrap and the machine-learning estimators).
4. Rebuild the web report from the new results:

   ```powershell
   .venv\Scripts\python.exe report\build_report.py
   ```
