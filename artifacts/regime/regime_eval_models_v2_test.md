# Regime-sliced results — `test` ('2026-06-01', '2026-11-03') — models `artifacts/models_v2`

Thresholds for the regime variables are fixed on the training period. Δ = log-loss improvement of the full model over the naive random walk, in millinats per decision, with a 95% day-block bootstrap CI.


## all

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| all | 44,352 | 0.5337 → 0.4900 | +43.7 [+38.2, +49.4] | 0.838 | 0.0144 | +36.1 | +41.5 | 0.616 |

## volatility regime (7-day)

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| calm | 29,664 | 0.5416 → 0.4923 | +49.3 [+41.4, +56.3] | 0.837 | 0.0167 | +41.8 | +48.0 | 0.625 |
| normal | 8,640 | 0.5269 → 0.4897 | +37.2 [+23.8, +49.5] | 0.837 | 0.0120 | +28.1 | +32.8 | 0.604 |
| turbulent | 6,048 | 0.5051 → 0.4795 | +25.6 [+18.2, +33.6] | 0.843 | 0.0095 | +20.1 | +22.1 | 0.587 |

## trend regime (7-day)

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| bear | 17,280 | 0.5246 → 0.4856 | +39.0 [+31.2, +47.8] | 0.840 | 0.0135 | +34.8 | +39.4 | 0.607 |
| sideways | 14,112 | 0.5531 → 0.4984 | +54.7 [+45.1, +65.8] | 0.833 | 0.0191 | +40.8 | +47.0 | 0.627 |
| bull | 12,960 | 0.5248 → 0.4868 | +38.0 [+30.1, +47.5] | 0.840 | 0.0117 | +32.9 | +38.5 | 0.613 |

## drawdown from 30-day high

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| deep (< -3 daily sd) | 16,704 | 0.5197 → 0.4841 | +35.6 [+29.9, +43.5] | 0.841 | 0.0132 | +32.8 | +37.0 | 0.607 |
| shallow | 27,648 | 0.5422 → 0.4936 | +48.6 [+41.1, +55.8] | 0.836 | 0.0164 | +38.2 | +44.2 | 0.621 |

## vol expansion (7d vs 30d)

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| expanding (> +0.3) | 5,472 | 0.4919 → 0.4704 | +21.5 [+15.0, +27.6] | 0.848 | 0.0107 | +21.3 | +23.2 | 0.583 |
| stable/contracting | 38,880 | 0.5396 → 0.4928 | +46.8 [+40.2, +54.5] | 0.836 | 0.0155 | +38.2 | +44.1 | 0.620 |

## intraday activity (1-hour vol)

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| quiet hour | 21,592 | 0.5855 → 0.5139 | +71.6 [+64.2, +78.8] | 0.824 | 0.0254 | +51.5 | +62.7 | 0.647 |
| normal hour | 16,091 | 0.4959 → 0.4711 | +24.8 [+21.6, +28.2] | 0.849 | 0.0058 | +26.5 | +27.5 | 0.601 |
| hot hour | 9,081 | 0.4743 → 0.4653 | +9.0 [+6.3, +11.8] | 0.851 | 0.0069 | +15.8 | +14.8 | 0.560 |

## calendar

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| weekday | 31,680 | 0.5095 → 0.4789 | +30.6 [+27.2, +34.7] | 0.844 | 0.0113 | +29.9 | +31.6 | 0.606 |
| weekend | 12,672 | 0.5944 → 0.5180 | +76.4 [+63.2, +89.6] | 0.822 | 0.0288 | +51.8 | +66.4 | 0.640 |
