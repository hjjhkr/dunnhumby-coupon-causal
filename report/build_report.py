"""Fill report/template.html with the numbers in outputs/results.json (written by the notebook).

Writes:
- deliverables/report.html     a complete web page you can open by double-clicking
- outputs/key_numbers.json     the headline numbers quoted in the report and the slides
- (optional) the path given as the first argument: the same page without the <html>/<head>
  shell, for online publishing

Run:  .venv\\Scripts\\python.exe report\\build_report.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = json.loads((ROOT / "outputs" / "results.json").read_text(encoding="utf-8"))

main, base = R["main"], R["main"]["base_level"]
win = main["windows"]
pct = lambda v: 100 * v / base

habit = R["habit"]
order = habit["order"]
ps = R["product_share"]
ps_a = next(v for k, v in ps["groups"].items() if k.startswith("TypeA"))
ps_a_during = next(r for r in ps["windows"] if r["campaign_type"].startswith("TypeA") and r["window_key"] == "during")
het = {r["key"]: r for r in R["heterogeneity"]}
sel8 = next(r for r in R["selection"]["table"] if r["campaign"] == 8)
power = R["power"]["table"]
n_1pct = next(r for r in power if r["lift"] == "1%")["households_per_group"]

K = dict(
    n_all=R["meta"]["n_households_all"], n_sample=R["meta"]["n_households_sample"], n_campaigns=R["meta"]["n_campaigns"],
    n_recipients=R["funnel"]["recipients"], n_mailings=R["funnel"]["mailings"], mailings_redeemed=R["funnel"]["mailings_redeemed"],
    mailing_rate=R["funnel"]["mailing_rate"], n_redeemers=R["funnel"]["redeemers"], never_redeemed=R["funnel"]["share_never_redeemed"],
    n_half=R["funnel"]["n_half"], n_half_share=R["funnel"]["n_half_share"],
    treated_before=R["naive"]["treated_before"], never_before=R["naive"]["never_before"],
    treated_after=R["naive"]["treated_after"], never_after=R["naive"]["never_after"],
    ratio_before=R["naive"]["ratio_before"], ratio_after=R["naive"]["ratio_after"],
    sel_auc=sel8["auc"], sel_lag=sel8["weeks_before_start"],
    mr_sel=R["mean_reversion"]["selection_window"], mr_between=R["mean_reversion"]["between"],
    mr_camp=R["mean_reversion"]["campaign"], mr_drop=R["mean_reversion"]["drop_pct"],
    base=base, n_treated=main["n_treated"],
    during_est=win["dr"]["during"]["est"], during_lo=win["dr"]["during"]["lo"], during_hi=win["dr"]["during"]["hi"],
    during_pct=pct(win["dr"]["during"]["est"]), during_pct_lo=pct(win["dr"]["during"]["lo"]), during_pct_hi=pct(win["dr"]["during"]["hi"]),
    holdout_pct=pct(win["dr"]["holdout"]["est"]), holdout_pct_lo=pct(win["dr"]["holdout"]["lo"]), holdout_pct_hi=pct(win["dr"]["holdout"]["hi"]),
    after_pct=pct(win["dr"]["after"]["est"]), after_pct_lo=pct(win["dr"]["after"]["lo"]), after_pct_hi=pct(win["dr"]["after"]["hi"]),
    did_holdout_pct=pct(win["did"]["holdout"]["est"]), did_during_pct=pct(win["did"]["during"]["est"]), did_after_pct=pct(win["did"]["after"]["est"]),
    ra_during_pct=pct(win["ra"]["during"]["est"]), eb_during_pct=pct(win["eb"]["during"]["est"]),
    smd_raw=R["balance"]["smd_raw_mean"], smd_adj=R["balance"]["smd_adj_max"],
    habit_same_product=habit["redeemed"][order[0]], habit_same_sub_only=habit["redeemed"][order[1]],
    habit_same_subcat=habit["same_subcat_redeemed"], habit_new_cat=habit["redeemed"][order[3]],
    habit_same_subcat_ordinary=habit["same_subcat_ordinary"], habit_new_cat_ordinary=habit["ordinary"][order[3]],
    mean_disc=R["discount"]["mean_disc"], mean_item=R["discount"]["mean_item_sales"],
    disc_share=R["discount"]["disc_share"], max_direct_share=R["discount"]["max_direct_share"],
    basket_with=R["discount"]["basket_with"], basket_without=R["discount"]["basket_without"],
    share_a_pre=ps_a["recipients_pre"], share_a_during=ps_a["recipients_during"],
    share_a_ddd=ps_a_during["change_pp"], share_a_ddd_lo=ps_a_during["lo"], share_a_ddd_hi=ps_a_during["hi"],
    share_a_usd_hi=ps_a_during["usd_hi"], share_a_mailings=ps_a["n_mailings"],
    redeemers_during=het["redeemers"]["during"], redeemers_holdout=het["redeemers"]["holdout"], redeemers_n=het["redeemers"]["households"],
    infreq_during=het["infrequent"]["during"],
    sd_change=R["power"]["sd_change"], mde_pct=R["power"]["mde_pct"], n_for_1pct=n_1pct, n_for_1pct_k=round(n_1pct / 1000),
)

c8 = R["selection"]["campaign8"]
weeks8 = sorted(int(k) for k in c8["p_by_active_weeks"])
robust = [dict(name=r["check"], n=r["treated"], est=r["during"], lo=r["during_lo"], hi=r["during_hi"])
          for r in R["robustness"]["table"] if r["during_hi"] - r["during_lo"] < 60]
ev = main["event"]

CHARTS = dict(
    selection=dict(weeks=weeks8, p=[c8["p_by_active_weeks"][str(k)] for k in weeks8], n=[c8["n_by_active_weeks"][str(k)] for k in weeks8]),
    mean_reversion=dict(n=R["mean_reversion"]["n"], weeks=R["mean_reversion"]["weeks"], weekly=R["mean_reversion"]["weekly"],
                        smooth=R["mean_reversion"]["smooth"]),
    levels=R["levels"],
    event=dict(ks=ev["ks"], dr=ev["dr"]["att"], dr_lo=ev["dr"]["lo"], dr_hi=ev["dr"]["hi"], did=ev["did"]["att"]),
    quintiles=[dict(label=r["quintile"], n=r["households"], spend=r["pre_spend"], share=r["redeem_share"]) for r in R["who_redeems"]["by_quintile"]],
    habit=dict(cats=order, redeemed=[habit["redeemed"][c] for c in order], ordinary=[habit["ordinary"][c] for c in order]),
    share=dict(ks=ps_a["ks"], ddd=ps_a["ddd"], lo=ps_a["lo"], hi=ps_a["hi"]),
    robust=robust,
    power=[dict(pct=r["lift"], usd=r["usd_per_week"], n=r["households_per_group"]) for r in power],
)


def rounded(o, nd=4):
    """Four decimals is plenty for chart data and keeps the file small."""
    if isinstance(o, dict):
        return {k: rounded(v, nd) for k, v in o.items()}
    if isinstance(o, list):
        return [rounded(v, nd) for v in o]
    if isinstance(o, float):
        return round(o, nd)
    return o


DATA = dict(k=K, charts=rounded(CHARTS))
template = (ROOT / "report" / "template.html").read_text(encoding="utf-8")

# Check: every number the template refers to must exist
missing = []
for path in sorted(set(re.findall(r'data-v="([^"]+)"', template))):
    node = DATA
    for part in path.split("."):
        node = node.get(part) if isinstance(node, dict) else None
    if node is None:
        missing.append(path)
if missing:
    sys.exit(f"The template refers to numbers that do not exist: {missing}")

body = template.replace("__DATA__", json.dumps(DATA, ensure_ascii=False).replace("</", "<\\/"))
head, rest = body.split('<div class="wrap">', 1)
standalone = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
              '<meta name="viewport" content="width=device-width, initial-scale=1">\n<style>body{margin:0}</style>\n'
              + head + '</head>\n<body>\n<div class="wrap">' + rest + '\n</body>\n</html>\n')
out = ROOT / "deliverables" / "report.html"
out.parent.mkdir(exist_ok=True)
out.write_text(standalone, encoding="utf-8")
(ROOT / "outputs" / "key_numbers.json").write_text(json.dumps(K, ensure_ascii=False, indent=1), encoding="utf-8")
if len(sys.argv) > 1:
    Path(sys.argv[1]).write_text(body, encoding="utf-8")

print(f"Wrote {out} ({len(standalone) / 1024:.0f} KB)")
for k, v in K.items():
    print(f"  {k:28s} {v:.4g}")
