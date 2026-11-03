# Out-of-sample report — split `test` ('2026-06-01', '2026-11-03')  (1,370,495 decision rows, 44,352 five-minute windows)


## Horizon T: 5-minute (to the window close)

### P(S(t+h) ≥ K) — above the fixed 5-minute reference

| model | log loss | Brier | AUC | ECE | accuracy |
|---|---|---|---|---|---|
| climatology | 0.6931 | 0.2500 | 0.5000 | 0.0072 | 0.501 |
| naive_rw | 0.5337 | 0.1679 | 0.8346 | 0.0399 | 0.743 |
| vol_only | 0.4962 | 0.1650 | 0.8362 | 0.0166 | 0.743 |
| structural | 0.4902 | 0.1640 | 0.8381 | 0.0152 | 0.744 |
| full | 0.4900 | 0.1642 | 0.8377 | 0.0144 | 0.744 |
| full+recal | 0.4875 | 0.1640 | 0.8376 | 0.0025 | 0.744 |

log-loss change from causal trailing recalibration (full -> full+recal): 2.589 millinats, 95% CI [1.476, 3.797]

log-loss improvement of `full` over `naive_rw`: 43.687 millinats/decision, 95% day-block CI [38.126, 49.827]

log-loss improvement of `full` over `structural`: 0.137 millinats/decision, 95% day-block CI [-0.539, 0.867]

By elapsed time in the window (log loss; skill = 1 - LL/LL_climatology-at-0.5):

| elapsed s | n | base | naive_rw | structural | full | full AUC | full acc |
|---|---|---|---|---|---|---|---|
| 0-0 | 44,352 | 0.6931 | 0.6932 | 0.6914 | 0.6937 | 0.528 | 0.520 |
| 1-59 | 261,695 | 0.6931 | 0.6615 | 0.6531 | 0.6547 | 0.652 | 0.604 |
| 60-119 | 266,112 | 0.6931 | 0.6064 | 0.5836 | 0.5848 | 0.756 | 0.686 |
| 120-179 | 266,112 | 0.6931 | 0.5391 | 0.5024 | 0.5030 | 0.832 | 0.752 |
| 180-239 | 266,112 | 0.6931 | 0.4634 | 0.4067 | 0.4064 | 0.897 | 0.815 |
| 240-299 | 266,112 | 0.6931 | 0.3739 | 0.2743 | 0.2702 | 0.959 | 0.898 |

Monthly consistency (log-loss improvement of full vs naive_rw, millinats):

| month | vs naive_rw | vs structural |
|---|---|---|
| 2026-06 | 31.82 | -0.14 |
| 2026-07 | 55.68 | 0.16 |
| 2026-08 | 37.24 | 2.18 |
| 2026-09 | 43.91 | -0.95 |
| 2026-10 | 50.08 | -0.54 |
| 2026-11 | 23.14 | -1.50 |

Reliability of `full` (all elapsed times):

| p bin | n | mean p | observed |
|---|---|---|---|
| 0.0-0.1 | 201,900 | 0.032 | 0.053 |
| 0.1-0.2 | 94,733 | 0.150 | 0.175 |
| 0.2-0.3 | 102,830 | 0.251 | 0.269 |
| 0.3-0.4 | 124,159 | 0.352 | 0.365 |
| 0.4-0.5 | 168,575 | 0.453 | 0.464 |
| 0.5-0.6 | 170,742 | 0.547 | 0.545 |
| 0.6-0.7 | 120,391 | 0.648 | 0.640 |
| 0.7-0.8 | 98,874 | 0.749 | 0.735 |
| 0.8-0.9 | 92,874 | 0.851 | 0.826 |
| 0.9-1.0 | 195,417 | 0.968 | 0.954 |

### Direction from *now*: P(S(t+h) > S(t)) (excl. unchanged, n=1,322,513)

| model | log loss (coin=0.6931) | AUC | accuracy |
|---|---|---|---|
| structural | 0.6861 | 0.5641 | 0.544 |
| full | 0.6869 | 0.5622 | 0.541 |

Information coefficient of the drift forecast: Pearson 0.0536, Spearman 0.0869
Top-decile-confidence directional accuracy: 0.637 (n=132,252)

### Volatility / speed of movement

| metric | naive (5-min RV) | model |
|---|---|---|
| QLIKE vs 5s-sampled realised var | 3.1778 | 1.5138 |
| corr(log forecast var, log realised var) | 0.6884 | 0.7491 |

### Magnitude: predictive quantiles of the log return (n=60,000)

| model | mean pinball (bps) | 50% interval coverage | 90% interval coverage | 90% width (bps) |
|---|---|---|---|---|
| naive_rw | 1.6708 | 0.451 | 0.781 | 12.34 |
| structural | 1.6187 | 0.512 | 0.894 | 17.37 |
| full | 1.6192 | 0.509 | 0.891 | 17.28 |

### Threshold probabilities at the horizon: P(S(t+h) ≥ K·(1+δ))

| δ (bps) | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|
| -20 | 0.964 | 0.1052 | 0.0838 | 0.0837 | 0.944 |
| -10 | 0.875 | 0.2561 | 0.2198 | 0.2198 | 0.910 |
| +10 | 0.124 | 0.2610 | 0.2189 | 0.2190 | 0.909 |
| +20 | 0.038 | 0.1078 | 0.0851 | 0.0850 | 0.943 |

### Touch probabilities: P(price reaches K·(1±δ) before the horizon ends | not there now)

| level | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| K+5bp | 1,145,295 | 0.232 | 0.4544 | 0.4138 | 0.3739 | 0.863 |
| K-5bp | 1,134,969 | 0.237 | 0.4551 | 0.4177 | 0.3767 | 0.864 |
| K+10bp | 1,276,013 | 0.129 | 0.3225 | 0.2723 | 0.2548 | 0.888 |
| K-10bp | 1,273,273 | 0.129 | 0.3125 | 0.2720 | 0.2519 | 0.892 |
| K+20bp | 1,346,632 | 0.043 | 0.1509 | 0.1199 | 0.1125 | 0.925 |
| K-20bp | 1,346,436 | 0.044 | 0.1474 | 0.1172 | 0.1097 | 0.930 |
| K+30bp | 1,362,091 | 0.018 | 0.0754 | 0.0588 | 0.0549 | 0.945 |
| K-30bp | 1,362,802 | 0.018 | 0.0725 | 0.0577 | 0.0531 | 0.948 |

### First passage from the current price: P(+δ first), P(−δ first), P(neither) within the horizon

| δ (bps) | n | P(up first) obs | naive 3-class LL | structural LL | full LL | up-vs-down AUC (decided rows) |
|---|---|---|---|---|---|---|
| 5 | 1,370,444 | 0.240 | 0.9124 | 0.8867 | 0.7510 | 0.572 |
| 10 | 1,370,490 | 0.110 | 0.6178 | 0.5312 | 0.4791 | 0.566 |
| 20 | 1,370,494 | 0.030 | 0.2542 | 0.2012 | 0.1812 | 0.597 |
| 30 | 1,370,495 | 0.011 | 0.1177 | 0.0933 | 0.0801 | 0.653 |

## Horizon 30: 30-second

### P(S(t+h) ≥ K) — above the fixed 5-minute reference (decision times whose horizon stays inside the window)

| model | log loss | Brier | AUC | ECE | accuracy |
|---|---|---|---|---|---|
| climatology | 0.6931 | 0.2500 | 0.5000 | 0.0106 | 0.503 |
| naive_rw | 0.3579 | 0.1069 | 0.9309 | 0.0306 | 0.852 |
| vol_only | 0.3398 | 0.1080 | 0.9318 | 0.0403 | 0.852 |
| structural | 0.3257 | 0.1034 | 0.9343 | 0.0117 | 0.850 |
| full | 0.3164 | 0.0996 | 0.9382 | 0.0023 | 0.858 |
| full+recal | 0.3163 | 0.0996 | 0.9382 | 0.0021 | 0.858 |

log-loss change from causal trailing recalibration (full -> full+recal): 0.021 millinats, 95% CI [-0.089, 0.127]

log-loss improvement of `full` over `naive_rw`: 41.536 millinats/decision, 95% day-block CI [37.769, 45.694]

log-loss improvement of `full` over `structural`: 9.359 millinats/decision, 95% day-block CI [6.669, 12.763]

By elapsed time in the window (log loss; skill = 1 - LL/LL_climatology-at-0.5):

| elapsed s | n | base | naive_rw | structural | full | full AUC | full acc |
|---|---|---|---|---|---|---|---|
| 0-0 | 44,352 | 0.6931 | 0.6932 | 0.6772 | 0.6700 | 0.618 | 0.581 |
| 1-59 | 261,695 | 0.6931 | 0.5030 | 0.4751 | 0.4611 | 0.862 | 0.776 |
| 60-119 | 266,112 | 0.6931 | 0.3668 | 0.3314 | 0.3205 | 0.937 | 0.863 |
| 120-179 | 266,112 | 0.6931 | 0.3033 | 0.2695 | 0.2613 | 0.958 | 0.893 |
| 180-239 | 266,112 | 0.6931 | 0.2551 | 0.2260 | 0.2191 | 0.971 | 0.912 |
| 240-299 | 137,473 | 0.6931 | 0.2609 | 0.2187 | 0.2134 | 0.972 | 0.918 |

Monthly consistency (log-loss improvement of full vs naive_rw, millinats):

| month | vs naive_rw | vs structural |
|---|---|---|
| 2026-06 | 25.18 | 1.30 |
| 2026-07 | 37.63 | 6.79 |
| 2026-08 | 54.06 | 20.52 |
| 2026-09 | 45.72 | 7.68 |
| 2026-10 | 43.71 | 9.57 |
| 2026-11 | 72.44 | 28.54 |

Reliability of `full` (all elapsed times):

| p bin | n | mean p | observed |
|---|---|---|---|
| 0.0-0.1 | 337,622 | 0.029 | 0.028 |
| 0.1-0.2 | 95,181 | 0.146 | 0.138 |
| 0.2-0.3 | 62,904 | 0.247 | 0.243 |
| 0.3-0.4 | 48,246 | 0.349 | 0.347 |
| 0.4-0.5 | 56,097 | 0.453 | 0.448 |
| 0.5-0.6 | 71,326 | 0.550 | 0.542 |
| 0.6-0.7 | 62,276 | 0.650 | 0.650 |
| 0.7-0.8 | 69,108 | 0.752 | 0.752 |
| 0.8-0.9 | 106,102 | 0.854 | 0.855 |
| 0.9-1.0 | 332,994 | 0.971 | 0.970 |

### Direction from *now*: P(S(t+h) > S(t)) (excl. unchanged, n=1,252,770)

| model | log loss (coin=0.6931) | AUC | accuracy |
|---|---|---|---|
| structural | 0.6713 | 0.6165 | 0.583 |
| full | 0.6719 | 0.6156 | 0.583 |

Information coefficient of the drift forecast: Pearson 0.1357, Spearman 0.1869
Top-decile-confidence directional accuracy: 0.712 (n=125,277)

### Volatility / speed of movement

| metric | naive (5-min RV) | model |
|---|---|---|
| QLIKE vs 5s-sampled realised var | 4.2041 | 2.7533 |
| corr(log forecast var, log realised var) | 0.5764 | 0.6262 |

### Magnitude: predictive quantiles of the log return (n=60,000)

| model | mean pinball (bps) | 50% interval coverage | 90% interval coverage | 90% width (bps) |
|---|---|---|---|---|
| naive_rw | 0.7513 | 0.508 | 0.801 | 6.04 |
| structural | 0.7251 | 0.548 | 0.896 | 7.93 |
| full | 0.7244 | 0.539 | 0.893 | 7.89 |

### Threshold probabilities at the horizon: P(S(t+h) ≥ K·(1+δ))

| δ (bps) | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|
| -20 | 0.979 | 0.0331 | 0.0279 | 0.0278 | 0.991 |
| -10 | 0.917 | 0.1085 | 0.0920 | 0.0919 | 0.979 |
| +10 | 0.081 | 0.1078 | 0.0901 | 0.0899 | 0.979 |
| +20 | 0.021 | 0.0343 | 0.0278 | 0.0277 | 0.991 |

### Touch probabilities: P(price reaches K·(1±δ) before the horizon ends | not there now)

| level | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| K+5bp | 1,145,295 | 0.076 | 0.2190 | 0.2049 | 0.1691 | 0.916 |
| K-5bp | 1,134,969 | 0.079 | 0.2299 | 0.2142 | 0.1761 | 0.913 |
| K+10bp | 1,276,013 | 0.036 | 0.1106 | 0.0983 | 0.0851 | 0.952 |
| K-10bp | 1,273,273 | 0.037 | 0.1120 | 0.1011 | 0.0866 | 0.952 |
| K+20bp | 1,346,632 | 0.011 | 0.0383 | 0.0325 | 0.0291 | 0.973 |
| K-20bp | 1,346,436 | 0.011 | 0.0365 | 0.0315 | 0.0281 | 0.977 |
| K+30bp | 1,362,091 | 0.005 | 0.0166 | 0.0140 | 0.0127 | 0.972 |
| K-30bp | 1,362,802 | 0.004 | 0.0155 | 0.0132 | 0.0118 | 0.980 |

### First passage from the current price: P(+δ first), P(−δ first), P(neither) within the horizon

| δ (bps) | n | P(up first) obs | naive 3-class LL | structural LL | full LL | up-vs-down AUC (decided rows) |
|---|---|---|---|---|---|---|
| 5 | 1,370,455 | 0.079 | 0.5274 | 0.4840 | 0.4143 | 0.629 |
| 10 | 1,370,487 | 0.018 | 0.1758 | 0.1457 | 0.1273 | 0.638 |
| 20 | 1,370,494 | 0.003 | 0.0352 | 0.0279 | 0.0232 | 0.720 |
| 30 | 1,370,495 | 0.001 | 0.0122 | 0.0099 | 0.0077 | 0.769 |

## Horizon 60: 1-minute

### P(S(t+h) ≥ K) — above the fixed 5-minute reference (decision times whose horizon stays inside the window)

| model | log loss | Brier | AUC | ECE | accuracy |
|---|---|---|---|---|---|
| climatology | 0.6932 | 0.2500 | 0.5000 | 0.0096 | 0.500 |
| naive_rw | 0.4562 | 0.1428 | 0.8790 | 0.0327 | 0.793 |
| vol_only | 0.4349 | 0.1426 | 0.8802 | 0.0347 | 0.793 |
| structural | 0.4253 | 0.1390 | 0.8837 | 0.0093 | 0.793 |
| full | 0.4201 | 0.1368 | 0.8870 | 0.0035 | 0.798 |
| full+recal | 0.4202 | 0.1368 | 0.8869 | 0.0027 | 0.798 |

log-loss change from causal trailing recalibration (full -> full+recal): -0.096 millinats, 95% CI [-0.207, 0.009]

log-loss improvement of `full` over `naive_rw`: 36.146 millinats/decision, 95% day-block CI [33.297, 39.337]

log-loss improvement of `full` over `structural`: 5.209 millinats/decision, 95% day-block CI [3.460, 7.448]

By elapsed time in the window (log loss; skill = 1 - LL/LL_climatology-at-0.5):

| elapsed s | n | base | naive_rw | structural | full | full AUC | full acc |
|---|---|---|---|---|---|---|---|
| 0-0 | 44,352 | 0.6931 | 0.6932 | 0.6842 | 0.6803 | 0.588 | 0.561 |
| 1-59 | 261,695 | 0.6931 | 0.5751 | 0.5526 | 0.5459 | 0.794 | 0.716 |
| 60-119 | 266,112 | 0.6931 | 0.4656 | 0.4310 | 0.4251 | 0.885 | 0.805 |
| 120-179 | 266,112 | 0.6931 | 0.3968 | 0.3618 | 0.3569 | 0.921 | 0.843 |
| 180-239 | 266,112 | 0.6931 | 0.3504 | 0.3159 | 0.3123 | 0.940 | 0.867 |
| 240-299 | 4,417 | 0.6931 | 0.4219 | 0.3532 | 0.3495 | 0.926 | 0.851 |

Monthly consistency (log-loss improvement of full vs naive_rw, millinats):

| month | vs naive_rw | vs structural |
|---|---|---|
| 2026-06 | 23.45 | 0.57 |
| 2026-07 | 32.45 | 3.54 |
| 2026-08 | 44.81 | 12.93 |
| 2026-09 | 41.06 | 3.58 |
| 2026-10 | 38.11 | 4.88 |
| 2026-11 | 54.39 | 15.95 |

Reliability of `full` (all elapsed times):

| p bin | n | mean p | observed |
|---|---|---|---|
| 0.0-0.1 | 199,454 | 0.039 | 0.038 |
| 0.1-0.2 | 101,943 | 0.147 | 0.143 |
| 0.2-0.3 | 81,530 | 0.249 | 0.238 |
| 0.3-0.4 | 72,201 | 0.350 | 0.347 |
| 0.4-0.5 | 85,665 | 0.453 | 0.451 |
| 0.5-0.6 | 98,022 | 0.549 | 0.547 |
| 0.6-0.7 | 84,912 | 0.650 | 0.654 |
| 0.7-0.8 | 89,893 | 0.751 | 0.758 |
| 0.8-0.9 | 102,293 | 0.852 | 0.851 |
| 0.9-1.0 | 192,887 | 0.961 | 0.960 |

### Direction from *now*: P(S(t+h) > S(t)) (excl. unchanged, n=1,311,123)

| model | log loss (coin=0.6931) | AUC | accuracy |
|---|---|---|---|
| structural | 0.6814 | 0.5850 | 0.560 |
| full | 0.6815 | 0.5846 | 0.560 |

Information coefficient of the drift forecast: Pearson 0.0975, Spearman 0.1319
Top-decile-confidence directional accuracy: 0.663 (n=131,113)

### Volatility / speed of movement

| metric | naive (5-min RV) | model |
|---|---|---|
| QLIKE vs 5s-sampled realised var | 3.2012 | 1.5631 |
| corr(log forecast var, log realised var) | 0.6091 | 0.6471 |

### Magnitude: predictive quantiles of the log return (n=60,000)

| model | mean pinball (bps) | 50% interval coverage | 90% interval coverage | 90% width (bps) |
|---|---|---|---|---|
| naive_rw | 1.1067 | 0.451 | 0.778 | 8.54 |
| structural | 1.0675 | 0.521 | 0.897 | 11.72 |
| full | 1.0673 | 0.517 | 0.894 | 11.68 |

### Threshold probabilities at the horizon: P(S(t+h) ≥ K·(1+δ))

| δ (bps) | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|
| -20 | 0.975 | 0.0552 | 0.0450 | 0.0449 | 0.979 |
| -10 | 0.905 | 0.1675 | 0.1405 | 0.1404 | 0.955 |
| +10 | 0.093 | 0.1670 | 0.1381 | 0.1380 | 0.955 |
| +20 | 0.025 | 0.0571 | 0.0453 | 0.0453 | 0.977 |

### Touch probabilities: P(price reaches K·(1±δ) before the horizon ends | not there now)

| level | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| K+5bp | 1,145,295 | 0.129 | 0.3247 | 0.2929 | 0.2587 | 0.886 |
| K-5bp | 1,134,969 | 0.134 | 0.3348 | 0.3016 | 0.2656 | 0.884 |
| K+10bp | 1,276,013 | 0.064 | 0.1838 | 0.1559 | 0.1424 | 0.927 |
| K-10bp | 1,273,273 | 0.065 | 0.1843 | 0.1588 | 0.1441 | 0.928 |
| K+20bp | 1,346,632 | 0.020 | 0.0700 | 0.0573 | 0.0529 | 0.960 |
| K-20bp | 1,346,436 | 0.021 | 0.0677 | 0.0555 | 0.0513 | 0.964 |
| K+30bp | 1,362,091 | 0.008 | 0.0321 | 0.0260 | 0.0240 | 0.967 |
| K-30bp | 1,362,802 | 0.008 | 0.0295 | 0.0242 | 0.0222 | 0.972 |

### First passage from the current price: P(+δ first), P(−δ first), P(neither) within the horizon

| δ (bps) | n | P(up first) obs | naive 3-class LL | structural LL | full LL | up-vs-down AUC (decided rows) |
|---|---|---|---|---|---|---|
| 5 | 1,370,442 | 0.149 | 0.7838 | 0.7301 | 0.6339 | 0.604 |
| 10 | 1,370,487 | 0.046 | 0.3594 | 0.2944 | 0.2662 | 0.609 |
| 20 | 1,370,494 | 0.008 | 0.0907 | 0.0717 | 0.0619 | 0.680 |
| 30 | 1,370,495 | 0.002 | 0.0335 | 0.0268 | 0.0218 | 0.739 |
