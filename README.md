# btc-movement — probabilistic Bitcoin model anchored on the fixed 5-minute reference price

This model gives a full, continuously updated probability picture of where Bitcoin goes **relative to the
fixed opening price of the current 5-minute candle**. It covers three horizons:

| capability | question answered (at every second *t* of the window) |
|---|---|
| **30-second** | where will BTC be at *t+30s*, relative to the reference *K* and to now? |
| **1-minute** | the same at *t+60s* |
| **5-minute** | where will BTC be at the 5-minute close, relative to *K*? |

For each horizon the engine outputs:

* **P(above / below the reference)** — `P(S(t+h) ≥ K)`
* **expected move and its uncertainty** — drift (bps), standard deviation (bps), and price quantiles 5/25/50/75/95 %
* **threshold probabilities** — `P(S(t+h) ≥ K·(1+δ))` for any δ (a full monotone conditional CDF)
* **touch probabilities** — `P(price reaches K·(1±δ) before the horizon ends)`, i.e. how likely each level is hit
* **which comes first** — `P(+δ first)`, `P(−δ first)`, `P(neither)` from the current price, within the horizon
* **speed** — forecast volatility per √second for the horizon

See **[REPORT.md](REPORT.md)** for the full out-of-sample evaluation.

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
* The 30s/60s horizons predict `S(t+30)` and `S(t+60)`. "Above the reference" compares them with the same
  fixed `K` of the window in which the decision is made.

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
            ┌──────────── per horizon h ∈ {30s, 60s, close} ────────────┐
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
python scripts/02_build_features.py --start 2024-02 --end 2026-11                    # sampled features
python scripts/03_train.py --frac 0.35                                               # ≈1 h on 4 cores
python scripts/04_evaluate.py --split test                                           # writes artifacts/models/report_test.md
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
{"ts": 1792074720, "window_start": 1792074600, "elapsed_s": 120, "remaining_s": 180,
 "reference_price": 81171.11, "price": 81035.58, "displacement_bps": -16.70,
 "horizons": {
  "close": {"p_above_reference": 0.1139, "p_above_reference_raw": 0.1105, "p_up_from_now": 0.5021,
            "expected_move_bps": 0.14, "sd_bps": 16.23, "vol_bps_per_sqrt_s": 1.21,
            "levels": {"K-10bp": {"price": 81089.98, "p_end_above": 0.31,   "p_touch_before_end": 0.5425},
                       "K+10bp": {"price": 81252.32, "p_end_above": 0.0365, "p_touch_before_end": 0.0549}},
            "first_passage_from_now": {"10bp": {"up_first": 0.409, "down_first": 0.402, "neither": 0.189}},
            "price_quantiles": {"q05": 80835.7, "q25": 80962.15, "q50": 81036.15, "q75": 81110.37, "q95": 81231.57}},
  "30s":   {"p_above_reference": 0.0043, "p_up_from_now": 0.4773, "expected_move_bps": -0.41, "sd_bps": 6.83, "...": "..."},
  "60s":   {"...": "..."}}}
```

* `p_above_reference` is the recalibrated probability that the horizon's price is ≥ K, and `_raw` is the value before
  recalibration. `levels` default to K±5/10/20/30 bps; any level can be queried through the engine API.
* `p_touch_before_end` is the probability that the price trades at that level at some point before the horizon
  ends. A level above the current price is reached from below, a level below it from above.
* `first_passage_from_now` is the probability of a +δ move before a −δ move from the current price (or neither) within
  the horizon.
* The prediction takes about 65–75 ms per second on one CPU core for all horizons and outputs.

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
scripts/                  01 download → 02 features → 03 train → 04 evaluate → 05/06/13 experiments →
                          07 walk-forward → 08 report → 09 replay → 10 recal → 11 production → 12 audit → 14 regimes
tests/                    look-ahead, structural-vs-Monte-Carlo, streaming-vs-batch
```
