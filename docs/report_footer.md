
## 8. Independent audit

`scripts/12_audit.py` recomputes the 5-minute labels and the naive baseline directly from the raw 1-second files,
sharing no code with the feature pipeline. On the test period:
* **0 mismatches** in K or in the window close over 1,370,489 decision rows (44,352 windows);
* ties (`close == K`) occur in 0.44% of windows;
* the up-rate is 49.9%;
* the naive log loss recomputed independently is 0.5346, against 0.5337 in the pipeline (rounding of the
  volatility proxy).

## 9. Limitations and honest caveats

* **Reference source.** The model is trained on Binance BTCUSDT spot. If your reference and settlement price
  comes from another source (Chainlink BTC/USD streams, Coinbase, an index), the lead-lag structure and the tie
  behaviour change. Rebuild the labels on that series; the pipeline is source-agnostic.
* **Latency.** The lead-lag edge lives at the 1–3 second scale. The live engine needs both feeds with low
  latency, and stale perp data silently removes most of the directional skill. Ablations show that removing
  the perp features costs about a third of the 30s drift IC.
* **Window-open direction is close to efficient.** At `e = 0` the 5-minute AUC is about 0.53, and the boosted
  head does not beat the analytic model there (validation and test agree). The value of the 5-minute model is in
  continuous re-pricing through the window, not in calling the direction at the open.
* **Calibration drift.** In 2026 the raw 5-minute model is slightly over-confident at the extremes. The causal
  14-day trailing recalibration removes this (ECE 0.012 → 0.003 on test). The live engine refits it daily from
  its own resolved predictions.
* **No transaction costs or market prices.** Log-loss gains are statistical skill. Turning them into profit
  against a real order book or prediction market depends on its prices, fees and latency, none of which are
  modelled here.
* **Regime risk.** Walk-forward folds cover May 2025 to Nov 2026, including very different volatility regimes,
  with consistent gains. A structural change in market microstructure (for example a venue migration of price
  discovery) would require retraining with `scripts/11_train_production.sh`.
