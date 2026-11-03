# Regime-sliced results — `test` ('2025-11-01', '2026-03-01') — models `artifacts/wf_B`

Thresholds for the regime variables are fixed on the training period. Δ = log-loss improvement of the full model over the naive random walk, in millinats per decision, with a 95% day-block bootstrap CI.


## all

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| all | 34,272 | 0.4799 → 0.4643 | +15.6 [+12.8, +18.4] | 0.853 | 0.0052 | +20.6 | +25.7 | 0.581 |

## volatility regime (7-day)

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| calm | 9,216 | 0.4807 → 0.4598 | +20.9 [+15.5, +25.7] | 0.856 | 0.0070 | +32.1 | +40.6 | 0.611 |
| normal | 14,688 | 0.4749 → 0.4602 | +14.7 [+11.2, +18.8] | 0.856 | 0.0079 | +20.7 | +25.8 | 0.583 |
| turbulent | 10,368 | 0.4863 → 0.4740 | +12.3 [+7.0, +18.4] | 0.846 | 0.0051 | +10.2 | +12.1 | 0.552 |

## trend regime (7-day)

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| bear | 18,144 | 0.4735 → 0.4626 | +10.9 [+8.1, +14.4] | 0.854 | 0.0063 | +15.3 | +18.7 | 0.568 |
| sideways | 10,944 | 0.4850 → 0.4650 | +19.9 [+14.9, +24.9] | 0.853 | 0.0067 | +25.0 | +32.3 | 0.594 |
| bull | 5,184 | 0.4915 → 0.4686 | +22.9 [+16.1, +29.4] | 0.850 | 0.0049 | +30.0 | +36.0 | 0.603 |

## drawdown from 30-day high

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| deep (< -3 daily sd) | 24,192 | 0.4790 → 0.4660 | +13.0 [+10.0, +16.9] | 0.852 | 0.0061 | +15.3 | +18.3 | 0.569 |
| shallow | 10,080 | 0.4820 → 0.4601 | +21.9 [+17.6, +26.5] | 0.856 | 0.0091 | +33.4 | +43.4 | 0.612 |

## vol expansion (7d vs 30d)

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| expanding (> +0.3) | 7,200 | 0.4725 → 0.4638 | +8.7 [+4.8, +12.6] | 0.852 | 0.0097 | +10.1 | +12.6 | 0.550 |
| stable/contracting | 27,072 | 0.4819 → 0.4644 | +17.4 [+14.1, +20.4] | 0.853 | 0.0055 | +23.4 | +29.2 | 0.589 |

## intraday activity (1-hour vol)

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| quiet hour | 9,406 | 0.5001 → 0.4679 | +32.2 [+28.4, +36.8] | 0.851 | 0.0081 | +44.4 | +58.3 | 0.634 |
| normal hour | 11,769 | 0.4844 → 0.4698 | +14.6 [+11.0, +18.6] | 0.850 | 0.0082 | +17.9 | +21.2 | 0.585 |
| hot hour | 14,805 | 0.4638 → 0.4578 | +6.0 [+3.7, +8.2] | 0.857 | 0.0094 | +7.8 | +8.6 | 0.544 |

## calendar

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| weekday | 24,480 | 0.4718 → 0.4610 | +10.8 [+8.4, +13.0] | 0.855 | 0.0080 | +15.3 | +18.4 | 0.572 |
| weekend | 9,792 | 0.5002 → 0.4726 | +27.7 [+21.4, +34.0] | 0.848 | 0.0066 | +33.9 | +43.8 | 0.607 |
