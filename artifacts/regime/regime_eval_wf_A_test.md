# Regime-sliced results — `test` ('2025-05-01', '2025-09-01') — models `artifacts/wf_A`

Thresholds for the regime variables are fixed on the training period. Δ = log-loss improvement of the full model over the naive random walk, in millinats per decision, with a 95% day-block bootstrap CI.


## all

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| all | 35,136 | 0.4714 → 0.4505 | +20.9 [+19.0, +23.0] | 0.863 | 0.0045 | +32.7 | +37.6 | 0.620 |

## volatility regime (7-day)

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| calm | 34,560 | 0.4714 → 0.4504 | +21.0 [+18.9, +23.0] | 0.863 | 0.0046 | +32.8 | +37.8 | 0.620 |
| normal | 576 | 0.4742 → 0.4570 | +17.2 [+13.7, +20.7] | 0.855 | 0.0214 | +25.4 | +29.5 | 0.620 |

## trend regime (7-day)

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| bear | 11,232 | 0.4708 → 0.4501 | +20.7 [+17.5, +24.1] | 0.863 | 0.0080 | +30.9 | +34.2 | 0.619 |
| sideways | 13,536 | 0.4738 → 0.4499 | +23.9 [+20.1, +27.6] | 0.863 | 0.0051 | +35.7 | +42.0 | 0.628 |
| bull | 10,368 | 0.4690 → 0.4517 | +17.2 [+14.4, +20.4] | 0.861 | 0.0061 | +30.7 | +35.7 | 0.610 |

## drawdown from 30-day high

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| deep (< -3 daily sd) | 8,064 | 0.4704 → 0.4486 | +21.8 [+18.8, +25.0] | 0.864 | 0.0106 | +35.4 | +39.7 | 0.626 |
| shallow | 27,072 | 0.4717 → 0.4511 | +20.6 [+18.0, +23.2] | 0.862 | 0.0053 | +31.9 | +37.0 | 0.618 |

## vol expansion (7d vs 30d)

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| expanding (> +0.3) | 3,168 | 0.4629 → 0.4462 | +16.8 [+12.7, +19.6] | 0.865 | 0.0088 | +27.4 | +31.1 | 0.612 |
| stable/contracting | 31,968 | 0.4723 → 0.4510 | +21.3 [+19.0, +23.4] | 0.862 | 0.0046 | +33.2 | +38.3 | 0.621 |

## intraday activity (1-hour vol)

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| quiet hour | 21,912 | 0.4736 → 0.4476 | +26.0 [+23.7, +28.9] | 0.865 | 0.0062 | +41.0 | +48.9 | 0.643 |
| normal hour | 11,288 | 0.4723 → 0.4569 | +15.4 [+12.7, +18.2] | 0.857 | 0.0035 | +22.6 | +23.3 | 0.591 |
| hot hour | 3,521 | 0.4545 → 0.4493 | +5.2 [+1.6, +8.7] | 0.862 | 0.0078 | +10.8 | +10.5 | 0.558 |

## calendar

| slice | windows | 5-min naive → full | Δ 5-min | 5-min AUC | 5-min ECE | 1-min Δ | 30s Δ | 30s dir. AUC |
|---|---|---|---|---|---|---|---|---|
| weekday | 25,056 | 0.4686 → 0.4500 | +18.6 [+16.3, +20.5] | 0.863 | 0.0042 | +28.5 | +30.9 | 0.612 |
| weekend | 10,080 | 0.4783 → 0.4518 | +26.6 [+22.8, +30.3] | 0.862 | 0.0074 | +43.1 | +54.3 | 0.641 |
