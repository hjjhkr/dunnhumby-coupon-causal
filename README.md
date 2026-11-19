# Do Coupons Create Sales, or Just Give Money Away?

Final project for a Causal Modeling course. Using dunnhumby's "The Complete Journey" (2,500 households, about two years of purchases, 30 coupon campaigns), we estimate the causal effect of targeted coupon campaigns on household spending.

## What we found

1. **No detectable lift.** After a first campaign, weekly spending changes by about +1% (95% confidence interval −8% to +11%).
2. **Simple comparisons mislead in both directions.** A direct comparison says recipients spend 4.5 times as much; a plain difference-in-differences says coupons cut spending by 4–10%. Both come from how the retailer selects households.
3. **Coupons mostly subsidized existing purchases.** 73% of recipient households never redeemed, and 82% of redeemed items were in a product sub-category the household had bought in the previous six months.
4. **The data cannot detect small effects.** Detecting a 1% lift would take about 72,000 households per group in a randomized test.

## What is in this repository

| Path | Contents |
|---|---|
| `coupon_causal_analysis.ipynb` | **The core deliverable.** The whole analysis, commented step by step, with all figures and results |
| `deliverables/report.html` | Story-style web report with interactive charts (open it in a browser) |
| `deliverables/slides/` | Source files of the slide deck |
| `report/` | Template and build script that turn the notebook's results into the web report |
| `outputs/figures/`, `outputs/tables/` | Figures and tables written by the notebook |
| `outputs/results.json` | Every number quoted in the report and the slides |
| `data/raw/` | The 8 raw CSV files (not in the repository, see below) |

## Method in one paragraph

The data is observational: the retailer sent coupons to its most frequent shoppers, chosen about four months ahead. For each cohort of households receiving a campaign for the first time, the control group is the households that had not received any campaign yet, weighted (entropy balancing) to match the treated on pre-campaign spending, trips and visit frequency. The effect is a doubly robust difference-in-differences. The last 8 weeks before each campaign are held out from the weighting and used as a check that the two groups move together.

## Reproducing the results

1. Download the data from [Kaggle](https://www.kaggle.com/datasets/frtgnn/dunnhumby-the-complete-journey) or the [dunnhumby source files page](https://www.dunnhumby.com/source-files/) and put the 8 CSV files in `data/raw/`. The data's terms of use do not allow redistribution, so it is not in this repository.
2. Create an environment and install the dependencies:

   ```powershell
   python -m venv .venv
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. Open `coupon_causal_analysis.ipynb` and run all cells (about 10 minutes; most of it is the bootstrap).
4. Rebuild the web report from the new results:

   ```powershell
   .venv\Scripts\python.exe report\build_report.py
   ```
