"""Assemble REPORT.md from the evaluation / ablation JSON files (no numbers are typed by hand)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "artifacts"


def load(p):
    p = A / p
    return json.load(open(p)) if p.exists() else None


main = load("models/report_test.json")
val = load("models/report_val.json")
wfs = {k: load(f"wf_{k}/report_test.json") for k in ("A", "B")}
abl = {h: load(f"ablation/ablation_{h}.json") for h in ("30", "60", "T")}
seq = {h: load(f"ablation/sequence_cnn_{h}.json") for h in ("30", "T")}
HN = {"T": "5-minute (to close)", "30": "30-second", "60": "1-minute"}
L = []
w = L.append


def f(x, n=4):
    return "–" if x is None else f"{x:.{n}f}"


def mn(d):
    return f"{d['mean']*1e3:+.1f} [{d['ci95'][0]*1e3:+.1f}, {d['ci95'][1]*1e3:+.1f}]"


w("# Out-of-sample results\n")
w(f"Main test period **{main['range'][0]} → {main['range'][1]}** ({main['rows']:,} decision rows). "
  "Nothing in this period was used for training, early stopping, feature selection, recalibration choices or "
  "hyper-parameters. Log loss is in nats; lower is better. Improvements are reported in **millinats per decision**, "
  "with **95% day-block bootstrap CIs** in brackets. A coin flip scores 0.6931.\n")
w("For calibration, `full+recal` adds the causal trailing recalibration. It is fitted each day on the previous "
  "14 days of resolved outcomes. Enabling it was decided on the validation period.\n")

# ---------------------------------------------------------------- headline
w("## 1. P(price ≥ fixed 5-minute reference) — every horizon\n")
w("| horizon | naive RW | structural | full | full+recal | Δ full vs naive | Δ full vs structural | AUC | accuracy | ECE (full+recal) |")
w("|---|---|---|---|---|---|---|---|---|---|")
for H in ("30", "60", "T"):
    r = main["horizons"].get(H)
    if not r:
        continue
    a = r["above_ref"]
    w(f"| {HN[H]} | {f(a['naive_rw']['logloss'])} | {f(a['structural']['logloss'])} | {f(a['full']['logloss'])} | "
      f"{f(a['full+recal']['logloss'])} | {mn(a['dll_vs_naive_rw'])} | {mn(a['dll_vs_structural'])} | "
      f"{f(a['full+recal']['auc'],3)} | {f(a['full+recal']['acc'],3)} | {f(a['full+recal']['ece'])} |")
w("\n*naive RW* is a driftless Gaussian random walk using the last 5 minutes' realised volatility, which is what most "
  "dashboards compute. *structural* is the analytic layer on top of the learned volatility, drift and shape. "
  "*full* adds the prior-boosted head. For 30s and 60s the table uses decision times whose horizon ends inside the "
  "window.\n")

r = main["horizons"]["T"]
w("### 5-minute model, continuously through the window (test)\n")
w("| elapsed (s) | n | naive RW | structural | full | full+recal | AUC | accuracy |")
w("|---|---|---|---|---|---|---|---|")
for b, d in r["above_ref_by_e"].items():
    w(f"| {b} | {d['n']:,} | {f(d['naive_rw'])} | {f(d['structural'])} | {f(d['full'])} | {f(d['full+recal'])} | {f(d['auc_full'],3)} | {f(d['acc_full'],3)} |")
w("\nAt `e=0` the price is exactly at the reference, so the forecast is purely directional. That is the hardest case, "
  "and it is reported separately.\n")

# ---------------------------------------------------------------- direction
w("## 2. Pure direction from *now* (displacement removed)\n")
w("This is P(S(t+h) > S(t)). It isolates genuine predictive power: no information comes from where the price sits "
  "relative to K.\n")
w("| horizon | log loss | AUC | accuracy | top-10%-confidence accuracy | IC (Spearman) |")
w("|---|---|---|---|---|---|")
for H in ("30", "60", "T"):
    d = main["horizons"][H]["direction"]
    w(f"| {HN[H]} | {f(d['full']['logloss'])} | {f(d['full']['auc'],3)} | {f(d['full']['acc'],3)} | {f(d['top_decile_acc'],3)} | {f(d['ic_spearman'],3)} |")

# ---------------------------------------------------------------- magnitude / speed
w("\n## 3. Magnitude and speed\n")
w("| horizon | QLIKE naive → model | corr(log σ̂², log RV) naive → model | pinball (bps) naive → full | 50% cov | 90% cov |")
w("|---|---|---|---|---|---|")
for H in ("30", "60", "T"):
    v = main["horizons"][H]["volatility"]; q = main["horizons"][H]["quantiles"]
    w(f"| {HN[H]} | {f(v['qlike_rv5_naive'],3)} → **{f(v['qlike_rv5_model'],3)}** | {f(v['corr_log_sd_rv5_naive'],3)} → **{f(v['corr_log_sd_rv5_model'],3)}** | "
      f"{f(q['naive_rw']['pinball_bps'],3)} → **{f(q['full']['pinball_bps'],3)}** | {f(q['full']['cov50'],3)} | {f(q['full']['cov90'],3)} |")

# ---------------------------------------------------------------- thresholds / touch / first passage
w("\n## 4. Levels: thresholds, touches, which comes first\n")
for H in ("30", "60", "T"):
    h = main["horizons"][H]
    w(f"### {HN[H]}\n")
    w("| question | n | base rate | naive LL | structural LL | full LL | full AUC |")
    w("|---|---|---|---|---|---|---|")
    for d, t in h["thresholds"].items():
        w(f"| end ≥ K{int(d):+d}bp | – | {t['base']:.3f} | {f(t['naive'])} | {f(t['structural'])} | **{f(t['full'])}** | {f(t['auc'],3)} |")
    for k, t in h["touch"].items():
        w(f"| touch {k} | {t['n']:,} | {t['base']:.3f} | {f(t['naive'])} | {f(t['structural'])} | **{f(t['full'])}** | {f(t['auc'],3)} |")
    for d, t in h["first_passage"].items():
        w(f"| ±{d}bp: which first (3-class) | {t['n']:,} | up-first {t['p_up_obs']:.3f} | {f(t['naive'])} | {f(t['structural'])} | **{f(t['full'])}** | {f(t['auc_up_vs_down'],3)} (up vs down) |")
    w("")

# ---------------------------------------------------------------- consistency
w("## 5. Consistency\n")
w("### Month by month (main test, 5-minute model, Δ log loss in millinats)\n")
w("| month | full vs naive RW | full vs structural |\n|---|---|---|")
for m, d in main["horizons"]["T"].get("above_ref_monthly", {}).items():
    w(f"| {m} | {d['vs_naive']*1e3:+.1f} | {d['vs_struct']*1e3:+.1f} |")
w("\n### Walk-forward (full retrain on an expanding window for each fold)\n")
w("| fold | test period | horizon | naive RW | full | full+recal | Δ full vs naive | dir. AUC |")
w("|---|---|---|---|---|---|---|---|")
folds = [("A", wfs["A"]), ("B", wfs["B"]), ("val", val), ("main", main)]
for name, rep in folds:
    if not rep:
        continue
    for H in ("30", "60", "T"):
        if H not in rep["horizons"]:
            continue
        a = rep["horizons"][H]["above_ref"]
        w(f"| {name} | {rep['range'][0]} → {rep['range'][1]} | {HN[H]} | {f(a['naive_rw']['logloss'])} | {f(a['full']['logloss'])} | "
          f"{f(a['full+recal']['logloss'])} | {mn(a['dll_vs_naive_rw'])} | {f(rep['horizons'][H]['direction']['full']['auc'],3)} |")
w("\n(`val` was used for early stopping, so it is slightly optimistic. It is shown for completeness.)\n")

# ---------------------------------------------------------------- ablations
w("## 6. What drives the predictions (ablations on the validation period)\n")
for H in ("30", "60", "T"):
    ab = abl.get(H)
    if not ab:
        continue
    base = ab["all"]
    w(f"### {HN[H]}\n")
    w("| feature set | drift IC | direction AUC | above-ref LL (structural) | Δ LL vs all (millinats) | vol QLIKE |")
    w("|---|---|---|---|---|---|")
    for k, d in ab.items():
        w(f"| {k} | {d['ic']:.4f} | {d['dir_auc']:.4f} | {d['above_ref_ll']:.5f} | {(d['above_ref_ll']-base['above_ref_ll'])*1e3:+.2f} | {d['vol_qlike']:.4f} |")
    if "ridge_ic" in base:
        w(f"\nA linear (ridge) drift model on the same features reaches IC {base['ridge_ic']:.4f} (AUC {base['ridge_dir_auc']:.4f}), "
          f"against {base['ic']:.4f} for LightGBM.\n")
    top = list(base.get("top_drift_features", {}).items())[:10]
    if top:
        w("Top drift features (gain share): " + ", ".join(f"`{k}` {v:.2f}" for k, v in top) + "\n")
w("### Architecture experiment: temporal CNN on raw 1-second sequences\n")
for H, s in seq.items():
    if s:
        w(f"- **{HN[H]}**: the CNN alone has IC {s['ic_B_cnn']:.4f}; LightGBM drift alone {s['ic_B_lgbm_drift']:.4f}; "
          f"the blend (weight on the CNN {s['blend_w_cnn']:.1f}, chosen on held-out days) {s['ic_B_blend']:.4f}. "
          f"Correlation between the two forecasts: {s['corr_cnn_lgbm']:.2f}.")
(ROOT / "REPORT_TABLES.md").write_text("\n".join(L) + "\n")
print("\n".join(L))
