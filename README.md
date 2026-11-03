# btc-movement — probabilistic Bitcoin model anchored on the fixed 5-minute reference price

This model gives a full, continuously updated probability picture of where Bitcoin goes **relative to the
fixed opening price of the current 5-minute candle**. It covers five horizons:

| capability | question answered (at every second *t* of the window) |
|---|---|
| **10-second** | where will BTC be at *t+10s*, relative to the reference *K* and to now? |
| **15-second** | the same at *t+15s* |
| **30-second** | the same at *t+30s* |
| **1-minute** | the same at *t+60s* |
| **5-minute** | where will BTC be at the 5-minute close, relative to *K*? |

Each horizon has its own model stack and its own independent out-of-sample evaluation.

For each horizon the engine outputs:

* **P(above / below the reference)** — `P(S(t+h) ≥ K)`
* **expected move and its uncertainty** — drift (bps), standard deviation (bps), and price quantiles 5/25/50/75/95 %
* **threshold probabilities** — `P(S(t+h) ≥ K·(1+δ))` for any δ (a full monotone conditional CDF)
* **touch probabilities** — `P(price reaches K·(1±δ) before the horizon ends)`, i.e. how likely each level is hit
* **which comes first** — `P(+δ first)`, `P(−δ first)`, `P(neither)` from the current price, within the horizon
* **speed** — forecast volatility per √second for the horizon

### Results at a glance (held-out test, 1 Jun – 2 Nov 2026, 44,352 windows never used in development)

| horizon | naive RW log loss | **model** log loss | Δ vs naive, millinats [95% CI]¹ | AUC | accuracy | direction-from-now AUC | top-10% direction accuracy |
|---|---|---|---|---|---|---|---|
| 10 s | 0.233 | **0.190** | +43.4 [+39.5, +47.7] | 0.978 | 92.0% | 0.658 | 76.7% |
| 15 s | 0.274 | **0.231** | +43.4 [+39.5, +47.7] | 0.967 | 90.1% | 0.644 | 74.8% |
| 30 s | 0.358 | **0.316** | +41.5 [+37.8, +45.7] | 0.938 | 85.8% | 0.616 | 71.2% |
| 1 min | 0.456 | **0.420** | +36.1 [+33.3, +39.3] | 0.887 | 79.8% | 0.585 | 66.3% |
| 5 min (to close) | 0.534 | **0.487** | +43.7 [+38.1, +49.8] | 0.838 | 74.4% | 0.562 | 63.7% |

These are `P(price ≥ fixed 5-minute reference)` probabilities, re-evaluated every ~10 s through every window. The 5-minute row uses the adaptive prior/head ensemble that ships in the live engine. The improvement over the naive random walk is positive in **every month** of every test period, in **three walk-forward retrains** (bull run, −43% crash, bear low and rebound) and in **every regime slice**: volatility, trend, drawdown, vol expansion, intraday activity and weekday/weekend. Full details are in [REPORT.md](REPORT.md).

¹ Δ is for the boosted head before recalibration. For the 5-minute horizon the adaptive ensemble adds a further +0.9 [+0.6, +1.2] millinats.


---

## 1. Problem definition (exact)

* Windows are aligned to the UTC clock: `[00:00, 00:05)`, `[00:05, 00:10)`, … (the standard 5-minute candles).
* The **reference price** `K` is the opening price of the window: the first trade of its first second
  (`open` of the first 1-second bar, identical to the 5-minute kline open on Binance). `K` is **fixed for
  the whole window**. It is never a rolling or recomputed price, and it is stored and tested as such
  (`tests/test_no_lookahead.py::test_reference_fixed_within_window`).
* A decision at elapsed second `e ∈ [0, 300)` uses only the 1-second bars that have already closed. The current
  price is `S = close` of the last completed second. The remaining time is `τ = 300 − e`.
* The 5-minute outcome is the window's closing price (the last trade of its last second). "Above" means
  `close ≥ K`, so ties count as up, as in the common "Up or Down" market convention.
* The 10s/15s/30s/60s horizons predict `S(t+h)`. "Above the reference" compares them with the same fixed `K`
  of the window in which the decision is made.

Data: Binance **BTCUSDT spot 1-second klines** (price, volume, trade count, taker-buy volume) plus the
**BTCUSDT USDT-margined perpetual** aggregated trades, rebuilt into 1-second bars. Both come from
`data.binance.vision`, the official public archive, SHA-256 verified. The data runs from January 2024 to
2 November 2026: about 89 million seconds and about 306,000 five-minute windows.

## 2. Architecture

```
 1-second spot bars ─┐
 1-second perp bars ─┼─► causal feature engine (≈125 features, all computed from bars < t)
 causal seasonality ─┘          │
                                ▼
            ┌──────── per horizon h ∈ {10s, 15s, 30s, 60s, close} ───────┐
            │ A. volatility engine   LightGBM-gamma → σ_h  (5s-sampled RV) │
            │ B. drift engine        LightGBM → μ_h = E[R_h]/σ_h            │
            │ C. shape               Student-t (ν, scale) per τ-bucket      │
            │ ── structural layer: analytic probabilities ──                │
            │    terminal CDF · reflection-principle touch ·                │
            │    exact two-sided first passage (images + Girsanov)          │
            │ D. prior-boosted heads (init_score = logit p_structural)      │
            │    D1 above-reference · D2 monotone conditional CDF ·          │
            │    D3 touch · D4 first passage (3-class)                      │
            └───────────────────────────────────────────────────────────────┘
                 30s & 60s (μ, σ) are stacked out-of-fold into the 5-minute model
```

Design principles:

1. **Physics first, ML second.** Most of the information about `P(close ≥ K)` is the current displacement
   `log(S/K)` measured in units of the *remaining* volatility `σ√τ`. The model builds this explicitly
   from a strong volatility forecast, a drift forecast and a fat-tailed shape. It then derives every
   probability analytically: the terminal CDF, touches via the reflection principle with drift, and
   first passage via an exact image-series formula verified against Monte Carlo in
   `tests/test_structural.py`.
2. **Boosting from the prior.** The LightGBM heads start from the structural log-odds (`init_score`) and
   learn only the correction. A head that cannot beat the prior on validation stops after a few trees and
   reduces to it, so there is no forced complexity.
3. **One distribution, many questions.** The D2 head is a single monotone-in-threshold model of
   `P(R_h ≥ q)` for *any* `q`. Above-reference, any price threshold and the quantiles all come from one
   coherent conditional distribution.
4. **Horizons that talk to each other.** The 30s and 60s drift and volatility forecasts have high
   signal-to-noise and capture the immediate predictable move. They are fed out-of-fold into the
   5-minute model.

### What actually predicts BTC at these horizons (findings)

* **Spot lags the perpetual by 1–3 seconds.** The correlation of the futures return in second *t−1* with
  the spot return in second *t* is ≈0.20, and spot's own 1-second returns are positively autocorrelated
  (ρ₁≈0.14). The perp–spot **basis deviation** from its recent mean is the single strongest directional
  feature. Its rank correlation with the next 30s standardised return is 0.09–0.21 in every quarter from
  2024 to 2026, so it is not decaying.
* **Taker order-flow imbalance** (spot and perp, 1–30s) and **short-term momentum** of the last 2–10
  seconds carry information beyond the basis.
* **Volatility is highly forecastable** from multi-scale realised variance, ranges, intensity
  (Hawkes-style exponentially decayed squared returns), within-window realised volatility and causal
  intraday seasonality. That seasonality includes the bursts at 1-, 5- and 15-minute clock marks.
* Because 1-second returns are autocorrelated, the summed squared 1-second returns understate the true
  variance of 30s–5m moves by 1.6–1.8×. The model therefore targets **5-second-sampled realised
  variance** and recalibrates the scale per remaining-time bucket.

## 3. Rigour protocol

* **Chronological splits with embargo.** Train Feb 2024 → Feb 2026 · validation Mar–May 2026 (early stopping
  and model choices) · **test Jun 1 → Nov 2 2026, never used for any decision**. The last day of each segment
  is dropped, so no label crosses a boundary.
* **Look-ahead tests.** Every feature at decision index *i* is recomputed after randomly corrupting all data at
  indices ≥ *i*; features must be bit-identical (`tests/test_no_lookahead.py`). A mutation test (making the
  current price `close[i]` instead of `close[i-1]`) is caught.
* **Causal everything.** Seasonality profiles use only previous days. Stage-A/B inputs to the heads are
  out-of-fold, using 3 contiguous time blocks with gaps. Trailing recalibration uses only resolved outcomes
  from earlier days.
* **No train/serve skew.** The live engine calls the very same `features.compute` on a rolling buffer, and a
  test proves the streaming features equal the batch features (`tests/test_live_replay.py`).
* **Honest baselines.** Climatology, a naive random walk using the last 5 minutes' realised volatility, a
  vol-only structural model and the full model are compared with proper scoring rules (log loss, Brier),
  discrimination (AUC), calibration (ECE, reliability tables), pinball loss / interval coverage and QLIKE.
  Results are broken down by elapsed time and by month. Confidence intervals come from a **day-block
  bootstrap**, because the 31 decision rows of a window share one outcome.
* **No calendar alpha.** Hour, weekday and minute-of-hour are allowed only in the volatility engine,
  never in directional models.

## 3b. Regime robustness

Bitcoin went through very different regimes in this data. There was a bull run to $124k (2025), a 43% crash to
$63k (Nov 2025 – Feb 2026), a bear low at $58k and a rebound to $87k (2026). The model handles regime change at
four levels:

1. **Regime-invariant inputs by construction.** Every return, flow and basis feature is standardised by the
   current volatility. A "2-sigma move" means the same thing in a calm and in a turbulent market, so the
   directional relationships transfer across regimes.
2. **Explicit, causal regime state for magnitude only.** `btcmove/regime.py` provides 7- and 30-day volatility,
   vol-of-vol, vol expansion and regime age, trend and drawdown, volume and liquidity regime, and perp basis and
   share, all computed from *previous days only*. These enter the volatility engine. They are deliberately
   kept out of the directional models: offered there, they were used as directional signals and hurt validation
   performance, because two years contain too few regimes to learn regime-dependent drift.
3. **Adaptation.** Training rows are recency-weighted with a 180-day half-life, chosen on validation. A causal
   recalibration is refitted daily on the last 14 days of resolved outcomes.
4. **Detection.** The live engine scores its own resolved predictions against the naive baseline. It raises a
   `regime_alert` (rolling 24h skill, a CUSUM on the 5-minute skill, calibration-slope bounds) that tells you
   when to retrain (`scripts/11_train_production.sh`).

Evaluation slices every test period by causal regime variables: volatility, trend, drawdown, vol expansion,
intraday activity and weekday/weekend. It also includes walk-forward retrains whose test periods are a bull
run, a crash and a bear-market rebound (see REPORT.md §5–6).

## 4. Usage

```bash
pip install -r requirements.txt
python scripts/01_download_build.py --spot --futures --start 2024-01 --end 2026-11   # ~10 GB raw → 1s npz
python scripts/02_build_features.py --start 2024-02 --end 2026-11                    # features + labels + regime table
python scripts/02b_build_extra_targets.py --horizons 10,15                           # labels for the 10s/15s horizons
python scripts/03_train.py --frac 0.35 --horizons 30,60,T                            # ≈45 min on 4 cores (v2 recipe)
python scripts/03_train.py --frac 0.3  --horizons 10,15                              # 10s / 15s stacks
python scripts/04_evaluate.py --split test --horizons T,30,60                        # artifacts/models/report_test.*
python scripts/04_evaluate.py --split test --horizons 10,15                          # merged into the same report
python scripts/14_regime_eval.py --split test                                        # regime-sliced results
python scripts/10_fit_recal.py                                                       # initial live recalibration
MAIN=models python scripts/08_make_report.py                                         # REPORT.md
python -m pytest tests -q
```

Live (needs access to Binance public websockets):

```python
from btcmove.live import LivePredictor, run_binance
run_binance(LivePredictor.from_artifacts("artifacts/models"), out_path="predictions.jsonl")
```

Each second emits one JSON record. This is a real (trimmed) output from replaying 2026-10-15 14:32:00 UTC through
the live engine (`scripts/09_replay_demo.py`). Two minutes into the window the price is 16.7 bps below
the reference:

```json
{"ts": 1792074720, "window_start": 1792074600, "elapsed_s": 120, "remaining_s": 180, "reference_price": 81171.11, "price": 81035.58, "displacement_bps": -16.7,
 "horizons": {
  "close": {"horizon_s": 180.0, "p_above_reference": 0.1212, "p_above_reference_raw": 0.1071, "p_above_reference_structural": 0.1132, "p_below_reference": 0.8788, "p_up_from_now": 0.4665, "expected_move_bps": -0.783, "sd_bps": 16.3784, "vol_bps_per_sqrt_s": 1.2208, "levels": {"K-10bp": {"price": 81089.98, "p_end_above": 0.2819, "p_touch_before_end": 0.5465}, "K+10bp": {"price": 81252.32, "p_end_above": 0.0325, "p_touch_before_end": 0.0559}}, "first_passage_from_now": {"10bp": {"up_first": 0.368, "down_first": 0.442, "neither": 0.19}}, "price_quantiles": {"q05": 80823.65, "q25": 80951.8, "q50": 81026.49, "q75": 81101.35, "q95": 81222.02}},
  "10s":   {"horizon_s": 10.0, "p_above_reference": 0.0009, "p_above_reference_raw": 0.0009, "p_above_reference_structural": 0.0038, "p_below_reference": 0.9991, "p_up_from_now": 0.4358, "expected_move_bps": -0.4494, "sd_bps": 4.7706, "vol_bps_per_sqrt_s": 1.5086, "levels": {"K-10bp": {"price": 81089.98, "p_end_above": 0.0292, "p_touch_before_end": 0.0417}, "K+10bp": {"price": 81252.32, "p_end_above": 0.0007, "p_touch_before_end": 0.0007}}, "first_passage_from_now": {"10bp": {"up_first": 0.007, "down_first": 0.014, "neither": 0.979}}, "price_quantiles": {"q05": 80988.63, "q25": 81018.88, "q50": 81032.49, "q75": 81046.2, "q95": 81077.26}},
  "15s": {"...": "..."}, "30s": {"...": "..."}, "60s": {"...": "..."}},
 "monitor": {"skill_24h_nats": {"10": null, "15": null, "30": null, "60": null, "T": null}, "cusum_5m": 0.0, "regime_alert": false, "reasons": []}}
```

* `p_above_reference` is the recalibrated probability that the horizon's price is ≥ K, and `_raw` is the value before
  recalibration. `levels` default to K±5/10/20/30 bps; any level can be queried through the engine API.
* `p_touch_before_end` is the probability that the price trades at that level at some point before the horizon
  ends. A level above the current price is reached from below, a level below it from above.
* `first_passage_from_now` is the probability of a +δ move before a −δ move from the current price (or neither) within
  the horizon.
* `p_above_reference_structural` is the analytic prior. For the 5-minute horizon the live recalibrator blends it with
  the boosted head (adaptive ensemble). `monitor` reports rolling skill against the naive baseline and the `regime_alert`.
* The prediction takes about 105 ms per second for all five horizons and every output.

## 5. Layout

```
btcmove/
  download.py, build.py   raw archive download + 1-second bar construction
  series.py               aligned spot/perp 1s series for any time range
  features.py             causal feature engine + labels + causal seasonality
  structural.py           analytic probability layer (t-CDF, touch, first passage)
  model.py                per-horizon stack (vol, drift, shape, prior-boosted heads)
  engine.py               horizons working together + JSON outputs
  recal.py                causal trailing recalibration
  regime.py               causal multi-day regime state (daily aggregates -> rg_* features)
  live.py                 rolling-buffer real-time predictor + Binance connector + replay
  metrics.py              scoring rules, calibration, day-block bootstrap
scripts/                  01 download → 02/02b features & labels → 03 train → 04 evaluate → 05/06/13/15 experiments →
                          07 walk-forward → 08 report → 09 replay → 10 recal → 11 production → 12 audit → 14 regimes
artifacts/models/         production models (v2 recipe, 5 horizons) + recal.json + reports
artifacts/models_v1/      reports of the v1 recipe (for comparison); artifacts/wf_*: walk-forward reports
tests/                    look-ahead, structural-vs-Monte-Carlo, streaming-vs-batch
```
