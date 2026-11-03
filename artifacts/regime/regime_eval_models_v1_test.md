# Regime-sliced results — `test` ('2026-06-01', '2026-11-03') — models `artifacts/models`

Thresholds for the regime variables are fixed on the training period. Δ = log-loss improvement of the full model over the naive random walk, in millinats per decision, with a 95% day-block bootstrap CI.


## all

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| all | 44,352 | 0.5337 → 0.4896 | +44.2 [+39.0, +49.7] | 0.838 | 0.0121 | +36.3 | +41.8 | 0.617 |

## volatility regime (7-day)

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| calm | 29,664 | 0.5416 → 0.4916 | +50.0 [+42.4, +57.1] | 0.838 | 0.0138 | +42.1 | +48.4 | 0.626 |
| normal | 8,640 | 0.5269 → 0.4894 | +37.5 [+24.5, +49.2] | 0.838 | 0.0098 | +28.0 | +32.8 | 0.605 |
| turbulent | 6,048 | 0.5051 → 0.4800 | +25.1 [+18.5, +32.3] | 0.843 | 0.0092 | +20.0 | +22.2 | 0.586 |

## trend regime (7-day)

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| bear | 17,280 | 0.5246 → 0.4848 | +39.9 [+32.1, +48.8] | 0.841 | 0.0114 | +35.1 | +39.6 | 0.608 |
| sideways | 14,112 | 0.5531 → 0.4981 | +54.9 [+45.1, +65.8] | 0.834 | 0.0171 | +40.9 | +47.3 | 0.628 |
| bull | 12,960 | 0.5248 → 0.4866 | +38.2 [+30.6, +47.4] | 0.840 | 0.0102 | +33.1 | +38.7 | 0.614 |

## drawdown from 30-day high

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| deep (< -3 daily sd) | 16,704 | 0.5197 → 0.4834 | +36.3 [+30.8, +44.0] | 0.842 | 0.0116 | +33.0 | +37.2 | 0.607 |
| shallow | 27,648 | 0.5422 → 0.4933 | +48.9 [+41.4, +56.0] | 0.836 | 0.0144 | +38.4 | +44.6 | 0.622 |

## vol expansion (7d vs 30d)

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| expanding (> +0.3) | 5,472 | 0.4919 → 0.4708 | +21.1 [+15.4, +26.5] | 0.848 | 0.0100 | +21.4 | +23.4 | 0.583 |
| stable/contracting | 38,880 | 0.5396 → 0.4922 | +47.4 [+41.1, +55.3] | 0.837 | 0.0131 | +38.4 | +44.4 | 0.621 |

## intraday activity (1-hour vol)

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| quiet hour | 21,592 | 0.5855 → 0.5132 | +72.3 [+65.0, +79.3] | 0.825 | 0.0224 | +51.9 | +63.1 | 0.649 |
| normal hour | 16,091 | 0.4959 → 0.4714 | +24.5 [+21.5, +27.8] | 0.849 | 0.0055 | +26.4 | +27.7 | 0.601 |
| hot hour | 9,081 | 0.4743 → 0.4641 | +10.3 [+7.3, +13.1] | 0.852 | 0.0042 | +16.0 | +15.0 | 0.559 |

## calendar

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| weekday | 31,680 | 0.5095 → 0.4783 | +31.1 [+27.7, +35.0] | 0.844 | 0.0091 | +29.9 | +31.8 | 0.607 |
| weekend | 12,672 | 0.5944 → 0.5176 | +76.8 [+63.7, +89.9] | 0.823 | 0.0255 | +52.3 | +66.7 | 0.642 |
