# Out-of-sample report — split `val` ('2026-03-01', '2026-06-01')  (809,850 decision rows, 26,208 five-minute windows)


## Horizon T: 5-minute (to the window close)

### P(S(t+h) ≥ K) — above the fixed 5-minute reference

| model | log loss | Brier | AUC | ECE | accuracy |
|---|---|---|---|---|---|
| climatology | 0.6931 | 0.2500 | 0.5000 | 0.0073 | 0.501 |
| naive_rw | 0.5698 | 0.1783 | 0.8151 | 0.0486 | 0.727 |
| vol_only | 0.5243 | 0.1739 | 0.8174 | 0.0110 | 0.727 |
| structural | 0.5200 | 0.1739 | 0.8188 | 0.0259 | 0.728 |
| full | 0.5190 | 0.1741 | 0.8182 | 0.0251 | 0.727 |
| full+recal | 0.5133 | 0.1735 | 0.8179 | 0.0051 | 0.727 |

log-loss change from causal trailing recalibration (full -> full+recal): 5.711 millinats, 95% CI [3.775, 7.623]

log-loss improvement of `full` over `naive_rw`: 50.845 millinats/decision, 95% day-block CI [42.551, 58.730]

log-loss improvement of `full` over `structural`: 0.970 millinats/decision, 95% day-block CI [0.195, 1.612]

By elapsed time in the window (log loss; skill = 1 - LL/LL_climatology-at-0.5):

| elapsed s | n | base | naive_rw | structural | full | full AUC | full acc |
|---|---|---|---|---|---|---|---|
| 0-0 | 26,208 | 0.6931 | 0.6932 | 0.6921 | 0.6930 | 0.527 | 0.521 |
| 1-59 | 154,650 | 0.6931 | 0.6643 | 0.6567 | 0.6575 | 0.645 | 0.599 |
| 60-119 | 157,248 | 0.6931 | 0.6158 | 0.5937 | 0.5944 | 0.744 | 0.675 |
| 120-179 | 157,248 | 0.6931 | 0.5653 | 0.5275 | 0.5280 | 0.812 | 0.732 |
| 180-239 | 157,248 | 0.6931 | 0.5176 | 0.4537 | 0.4531 | 0.873 | 0.790 |
| 240-299 | 157,248 | 0.6931 | 0.4671 | 0.3418 | 0.3352 | 0.941 | 0.873 |

Monthly consistency (log-loss improvement of full vs naive_rw, millinats):

| month | vs naive_rw | vs structural |
|---|---|---|
| 2026-03 | 46.59 | 1.96 |
| 2026-04 | 44.45 | 0.53 |
| 2026-05 | 61.64 | 0.39 |

Reliability of `full` (all elapsed times):

| p bin | n | mean p | observed |
|---|---|---|---|
| 0.0-0.1 | 111,590 | 0.032 | 0.065 |
| 0.1-0.2 | 54,118 | 0.150 | 0.188 |
| 0.2-0.3 | 60,619 | 0.252 | 0.282 |
| 0.3-0.4 | 75,200 | 0.352 | 0.371 |
| 0.4-0.5 | 101,148 | 0.453 | 0.466 |
| 0.5-0.6 | 104,536 | 0.547 | 0.537 |
| 0.6-0.7 | 75,397 | 0.648 | 0.629 |
| 0.7-0.8 | 60,634 | 0.748 | 0.715 |
| 0.8-0.9 | 55,747 | 0.850 | 0.810 |
| 0.9-1.0 | 110,861 | 0.967 | 0.937 |

### Direction from *now*: P(S(t+h) > S(t)) (excl. unchanged, n=790,877)

| model | log loss (coin=0.6931) | AUC | accuracy |
|---|---|---|---|
| structural | 0.6883 | 0.5527 | 0.533 |
| full | 0.6888 | 0.5526 | 0.532 |

Information coefficient of the drift forecast: Pearson 0.0440, Spearman 0.0685
Top-decile-confidence directional accuracy: 0.621 (n=79,088)

### Volatility / speed of movement

| metric | naive (5-min RV) | model |
|---|---|---|
| QLIKE vs 5s-sampled realised var | 1.8891 | 1.2303 |
| corr(log forecast var, log realised var) | 0.6761 | 0.7356 |

### Magnitude: predictive quantiles of the log return (n=30,000)

| model | mean pinball (bps) | 50% interval coverage | 90% interval coverage | 90% width (bps) |
|---|---|---|---|---|
| naive_rw | 1.8588 | 0.467 | 0.803 | 15.21 |
| structural | 1.8183 | 0.519 | 0.900 | 20.97 |
| full | 1.8174 | 0.516 | 0.895 | 20.79 |

### Threshold probabilities at the horizon: P(S(t+h) ≥ K·(1+δ))

| δ (bps) | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|
| -20 | 0.956 | 0.1185 | 0.1000 | 0.0999 | 0.934 |
| -10 | 0.863 | 0.2761 | 0.2438 | 0.2438 | 0.897 |
| +10 | 0.139 | 0.2723 | 0.2428 | 0.2425 | 0.899 |
| +20 | 0.043 | 0.1145 | 0.0976 | 0.0972 | 0.935 |

### Touch probabilities: P(price reaches K·(1±δ) before the horizon ends | not there now)

| level | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| K+5bp | 658,631 | 0.265 | 0.4738 | 0.4581 | 0.4103 | 0.852 |
| K-5bp | 658,281 | 0.265 | 0.4798 | 0.4644 | 0.4133 | 0.849 |
| K+10bp | 745,164 | 0.152 | 0.3480 | 0.3153 | 0.2899 | 0.877 |
| K-10bp | 743,841 | 0.149 | 0.3519 | 0.3201 | 0.2915 | 0.874 |
| K+20bp | 793,163 | 0.052 | 0.1675 | 0.1436 | 0.1333 | 0.914 |
| K-20bp | 792,574 | 0.053 | 0.1709 | 0.1442 | 0.1331 | 0.916 |
| K+30bp | 804,000 | 0.021 | 0.0876 | 0.0736 | 0.0676 | 0.927 |
| K-30bp | 803,786 | 0.023 | 0.0952 | 0.0752 | 0.0692 | 0.932 |

### First passage from the current price: P(+δ first), P(−δ first), P(neither) within the horizon

| δ (bps) | n | P(up first) obs | naive 3-class LL | structural LL | full LL | up-vs-down AUC (decided rows) |
|---|---|---|---|---|---|---|
| 5 | 809,836 | 0.275 | 0.9725 | 1.0063 | 0.8197 | 0.569 |
| 10 | 809,848 | 0.132 | 0.6995 | 0.6482 | 0.5638 | 0.559 |
| 20 | 809,850 | 0.037 | 0.3110 | 0.2596 | 0.2303 | 0.602 |
| 30 | 809,850 | 0.013 | 0.1486 | 0.1199 | 0.1033 | 0.662 |

## Horizon 30: 30-second

### P(S(t+h) ≥ K) — above the fixed 5-minute reference (decision times whose horizon stays inside the window)

| model | log loss | Brier | AUC | ECE | accuracy |
|---|---|---|---|---|---|
| climatology | 0.6931 | 0.2500 | 0.5000 | 0.0085 | 0.504 |
| naive_rw | 0.3453 | 0.1052 | 0.9322 | 0.0206 | 0.851 |
| vol_only | 0.3351 | 0.1063 | 0.9331 | 0.0357 | 0.851 |
| structural | 0.3225 | 0.1023 | 0.9356 | 0.0093 | 0.852 |
| full | 0.3187 | 0.1008 | 0.9372 | 0.0049 | 0.856 |
| full+recal | 0.3181 | 0.1008 | 0.9372 | 0.0021 | 0.856 |

log-loss change from causal trailing recalibration (full -> full+recal): 0.519 millinats, 95% CI [0.297, 0.695]

log-loss improvement of `full` over `naive_rw`: 26.614 millinats/decision, 95% day-block CI [23.699, 29.823]

log-loss improvement of `full` over `structural`: 3.855 millinats/decision, 95% day-block CI [2.710, 5.227]

By elapsed time in the window (log loss; skill = 1 - LL/LL_climatology-at-0.5):

| elapsed s | n | base | naive_rw | structural | full | full AUC | full acc |
|---|---|---|---|---|---|---|---|
| 0-0 | 26,208 | 0.6931 | 0.6933 | 0.6835 | 0.6795 | 0.591 | 0.569 |
| 1-59 | 154,650 | 0.6931 | 0.4832 | 0.4634 | 0.4576 | 0.864 | 0.780 |
| 60-119 | 157,248 | 0.6931 | 0.3391 | 0.3196 | 0.3154 | 0.939 | 0.864 |
| 120-179 | 157,248 | 0.6931 | 0.2835 | 0.2630 | 0.2595 | 0.959 | 0.892 |
| 180-239 | 157,248 | 0.6931 | 0.2447 | 0.2247 | 0.2221 | 0.970 | 0.909 |
| 240-299 | 81,222 | 0.6931 | 0.2967 | 0.2482 | 0.2456 | 0.964 | 0.904 |

Monthly consistency (log-loss improvement of full vs naive_rw, millinats):

| month | vs naive_rw | vs structural |
|---|---|---|
| 2026-03 | 15.97 | 1.09 |
| 2026-04 | 26.23 | 3.69 |
| 2026-05 | 38.00 | 6.87 |

Reliability of `full` (all elapsed times):

| p bin | n | mean p | observed |
|---|---|---|---|
| 0.0-0.1 | 189,995 | 0.029 | 0.025 |
| 0.1-0.2 | 58,734 | 0.146 | 0.136 |
| 0.2-0.3 | 40,773 | 0.247 | 0.240 |
| 0.3-0.4 | 31,852 | 0.348 | 0.346 |
| 0.4-0.5 | 34,195 | 0.453 | 0.441 |
| 0.5-0.6 | 44,046 | 0.550 | 0.549 |
| 0.6-0.7 | 37,943 | 0.650 | 0.649 |
| 0.7-0.8 | 42,548 | 0.752 | 0.756 |
| 0.8-0.9 | 63,128 | 0.853 | 0.861 |
| 0.9-1.0 | 190,610 | 0.970 | 0.974 |

### Direction from *now*: P(S(t+h) > S(t)) (excl. unchanged, n=760,288)

| model | log loss (coin=0.6931) | AUC | accuracy |
|---|---|---|---|
| structural | 0.6759 | 0.6031 | 0.572 |
| full | 0.6760 | 0.6030 | 0.572 |

Information coefficient of the drift forecast: Pearson 0.1216, Spearman 0.1637
Top-decile-confidence directional accuracy: 0.695 (n=76,029)

### Volatility / speed of movement

| metric | naive (5-min RV) | model |
|---|---|---|
| QLIKE vs 5s-sampled realised var | 2.7347 | 2.1758 |
| corr(log forecast var, log realised var) | 0.5248 | 0.5719 |

### Magnitude: predictive quantiles of the log return (n=30,000)

| model | mean pinball (bps) | 50% interval coverage | 90% interval coverage | 90% width (bps) |
|---|---|---|---|---|
| naive_rw | 0.8475 | 0.497 | 0.816 | 7.42 |
| structural | 0.8215 | 0.533 | 0.905 | 9.47 |
| full | 0.8212 | 0.527 | 0.902 | 9.44 |

### Threshold probabilities at the horizon: P(S(t+h) ≥ K·(1+δ))

| δ (bps) | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|
| -20 | 0.974 | 0.0402 | 0.0338 | 0.0337 | 0.989 |
| -10 | 0.905 | 0.1247 | 0.1074 | 0.1072 | 0.974 |
| +10 | 0.094 | 0.1218 | 0.1058 | 0.1056 | 0.975 |
| +20 | 0.025 | 0.0414 | 0.0341 | 0.0340 | 0.987 |

### Touch probabilities: P(price reaches K·(1±δ) before the horizon ends | not there now)

| level | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| K+5bp | 658,631 | 0.092 | 0.2516 | 0.2438 | 0.1994 | 0.904 |
| K-5bp | 658,281 | 0.092 | 0.2534 | 0.2450 | 0.2004 | 0.903 |
| K+10bp | 745,164 | 0.045 | 0.1341 | 0.1221 | 0.1053 | 0.942 |
| K-10bp | 743,841 | 0.045 | 0.1344 | 0.1224 | 0.1053 | 0.941 |
| K+20bp | 793,163 | 0.014 | 0.0505 | 0.0431 | 0.0385 | 0.965 |
| K-20bp | 792,574 | 0.014 | 0.0472 | 0.0407 | 0.0362 | 0.971 |
| K+30bp | 804,000 | 0.005 | 0.0217 | 0.0185 | 0.0167 | 0.964 |
| K-30bp | 803,786 | 0.006 | 0.0213 | 0.0174 | 0.0157 | 0.977 |

### First passage from the current price: P(+δ first), P(−δ first), P(neither) within the horizon

| δ (bps) | n | P(up first) obs | naive 3-class LL | structural LL | full LL | up-vs-down AUC (decided rows) |
|---|---|---|---|---|---|---|
| 5 | 809,837 | 0.098 | 0.6136 | 0.5983 | 0.4969 | 0.624 |
| 10 | 809,848 | 0.024 | 0.2301 | 0.1932 | 0.1687 | 0.645 |
| 20 | 809,850 | 0.003 | 0.0507 | 0.0403 | 0.0323 | 0.741 |
| 30 | 809,850 | 0.001 | 0.0162 | 0.0134 | 0.0100 | 0.825 |

## Horizon 60: 1-minute

### P(S(t+h) ≥ K) — above the fixed 5-minute reference (decision times whose horizon stays inside the window)

| model | log loss | Brier | AUC | ECE | accuracy |
|---|---|---|---|---|---|
| climatology | 0.6931 | 0.2500 | 0.5000 | 0.0092 | 0.502 |
| naive_rw | 0.4418 | 0.1406 | 0.8815 | 0.0216 | 0.792 |
| vol_only | 0.4298 | 0.1406 | 0.8832 | 0.0333 | 0.792 |
| structural | 0.4211 | 0.1376 | 0.8861 | 0.0107 | 0.795 |
| full | 0.4194 | 0.1369 | 0.8870 | 0.0068 | 0.797 |
| full+recal | 0.4191 | 0.1369 | 0.8870 | 0.0030 | 0.797 |

log-loss change from causal trailing recalibration (full -> full+recal): 0.313 millinats, 95% CI [0.084, 0.505]

log-loss improvement of `full` over `naive_rw`: 22.433 millinats/decision, 95% day-block CI [20.261, 24.839]

log-loss improvement of `full` over `structural`: 1.729 millinats/decision, 95% day-block CI [1.208, 2.362]

By elapsed time in the window (log loss; skill = 1 - LL/LL_climatology-at-0.5):

| elapsed s | n | base | naive_rw | structural | full | full AUC | full acc |
|---|---|---|---|---|---|---|---|
| 0-0 | 26,208 | 0.6931 | 0.6932 | 0.6904 | 0.6879 | 0.560 | 0.544 |
| 1-59 | 154,650 | 0.6931 | 0.5592 | 0.5445 | 0.5421 | 0.797 | 0.718 |
| 60-119 | 157,248 | 0.6931 | 0.4379 | 0.4176 | 0.4158 | 0.891 | 0.808 |
| 120-179 | 157,248 | 0.6931 | 0.3774 | 0.3561 | 0.3546 | 0.922 | 0.841 |
| 180-239 | 157,248 | 0.6931 | 0.3517 | 0.3233 | 0.3221 | 0.936 | 0.861 |
| 240-299 | 2,598 | 0.6931 | 0.5027 | 0.4229 | 0.4225 | 0.894 | 0.812 |

Monthly consistency (log-loss improvement of full vs naive_rw, millinats):

| month | vs naive_rw | vs structural |
|---|---|---|
| 2026-03 | 14.24 | 0.77 |
| 2026-04 | 22.40 | 1.78 |
| 2026-05 | 30.94 | 2.67 |

Reliability of `full` (all elapsed times):

| p bin | n | mean p | observed |
|---|---|---|---|
| 0.0-0.1 | 110,134 | 0.040 | 0.032 |
| 0.1-0.2 | 60,649 | 0.148 | 0.132 |
| 0.2-0.3 | 50,903 | 0.249 | 0.241 |
| 0.3-0.4 | 45,805 | 0.349 | 0.347 |
| 0.4-0.5 | 52,803 | 0.453 | 0.450 |
| 0.5-0.6 | 60,262 | 0.548 | 0.550 |
| 0.6-0.7 | 50,471 | 0.650 | 0.653 |
| 0.7-0.8 | 53,404 | 0.751 | 0.761 |
| 0.8-0.9 | 60,983 | 0.852 | 0.861 |
| 0.9-1.0 | 109,786 | 0.960 | 0.965 |

### Direction from *now*: P(S(t+h) > S(t)) (excl. unchanged, n=789,651)

| model | log loss (coin=0.6931) | AUC | accuracy |
|---|---|---|---|
| structural | 0.6852 | 0.5696 | 0.549 |
| full | 0.6853 | 0.5698 | 0.549 |

Information coefficient of the drift forecast: Pearson 0.0881, Spearman 0.1140
Top-decile-confidence directional accuracy: 0.639 (n=78,966)

### Volatility / speed of movement

| metric | naive (5-min RV) | model |
|---|---|---|
| QLIKE vs 5s-sampled realised var | 1.7440 | 1.1259 |
| corr(log forecast var, log realised var) | 0.5526 | 0.5981 |

### Magnitude: predictive quantiles of the log return (n=30,000)

| model | mean pinball (bps) | 50% interval coverage | 90% interval coverage | 90% width (bps) |
|---|---|---|---|---|
| naive_rw | 1.2289 | 0.463 | 0.804 | 10.50 |
| structural | 1.1953 | 0.530 | 0.911 | 13.99 |
| full | 1.1947 | 0.526 | 0.907 | 13.93 |

### Threshold probabilities at the horizon: P(S(t+h) ≥ K·(1+δ))

| δ (bps) | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|
| -20 | 0.969 | 0.0683 | 0.0555 | 0.0554 | 0.973 |
| -10 | 0.892 | 0.1879 | 0.1617 | 0.1616 | 0.946 |
| +10 | 0.107 | 0.1829 | 0.1594 | 0.1591 | 0.947 |
| +20 | 0.030 | 0.0669 | 0.0546 | 0.0544 | 0.971 |

### Touch probabilities: P(price reaches K·(1±δ) before the horizon ends | not there now)

| level | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| K+5bp | 658,631 | 0.153 | 0.3591 | 0.3391 | 0.2964 | 0.872 |
| K-5bp | 658,281 | 0.153 | 0.3627 | 0.3428 | 0.2989 | 0.869 |
| K+10bp | 745,164 | 0.078 | 0.2130 | 0.1893 | 0.1717 | 0.914 |
| K-10bp | 743,841 | 0.078 | 0.2154 | 0.1909 | 0.1725 | 0.913 |
| K+20bp | 793,163 | 0.025 | 0.0891 | 0.0737 | 0.0677 | 0.948 |
| K-20bp | 792,574 | 0.025 | 0.0871 | 0.0716 | 0.0657 | 0.952 |
| K+30bp | 804,000 | 0.010 | 0.0408 | 0.0341 | 0.0312 | 0.956 |
| K-30bp | 803,786 | 0.010 | 0.0407 | 0.0326 | 0.0300 | 0.965 |

### First passage from the current price: P(+δ first), P(−δ first), P(neither) within the horizon

| δ (bps) | n | P(up first) obs | naive 3-class LL | structural LL | full LL | up-vs-down AUC (decided rows) |
|---|---|---|---|---|---|---|
| 5 | 809,836 | 0.179 | 0.8750 | 0.8710 | 0.7274 | 0.599 |
| 10 | 809,848 | 0.057 | 0.4401 | 0.3782 | 0.3384 | 0.610 |
| 20 | 809,850 | 0.010 | 0.1266 | 0.0999 | 0.0848 | 0.702 |
| 30 | 809,850 | 0.003 | 0.0465 | 0.0372 | 0.0294 | 0.766 |
