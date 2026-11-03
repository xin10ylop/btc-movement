# Out-of-sample report — split `test` ('2026-06-01', '2026-11-03')  (1,370,495 decision rows, 44,352 five-minute windows)


## Horizon T: 5-minute (to the window close)

### P(S(t+h) ≥ K) — above the fixed 5-minute reference

| model | log loss | Brier | AUC | ECE | accuracy |
|---|---|---|---|---|---|
| climatology | 0.6931 | 0.2500 | 0.5000 | 0.0072 | 0.501 |
| naive_rw | 0.5337 | 0.1679 | 0.8346 | 0.0399 | 0.743 |
| vol_only | 0.4961 | 0.1650 | 0.8362 | 0.0167 | 0.743 |
| structural | 0.4900 | 0.1640 | 0.8381 | 0.0141 | 0.744 |
| full | 0.4896 | 0.1639 | 0.8384 | 0.0121 | 0.745 |
| full+recal | 0.4867 | 0.1637 | 0.8383 | 0.0027 | 0.745 |

log-loss change from causal trailing recalibration (full -> full+recal): 2.879 millinats, 95% CI [1.730, 4.049]

log-loss improvement of `full` over `naive_rw`: 44.167 millinats/decision, 95% day-block CI [38.926, 50.181]

log-loss improvement of `full` over `structural`: 0.466 millinats/decision, 95% day-block CI [-0.186, 1.189]

By elapsed time in the window (log loss; skill = 1 - LL/LL_climatology-at-0.5):

| elapsed s | n | base | naive_rw | structural | full | full AUC | full acc |
|---|---|---|---|---|---|---|---|
| 0-0 | 44,352 | 0.6931 | 0.6932 | 0.6916 | 0.6926 | 0.530 | 0.524 |
| 1-59 | 261,695 | 0.6931 | 0.6615 | 0.6530 | 0.6537 | 0.653 | 0.605 |
| 60-119 | 266,112 | 0.6931 | 0.6064 | 0.5834 | 0.5836 | 0.757 | 0.687 |
| 120-179 | 266,112 | 0.6931 | 0.5391 | 0.5021 | 0.5016 | 0.833 | 0.753 |
| 180-239 | 266,112 | 0.6931 | 0.4634 | 0.4068 | 0.4060 | 0.897 | 0.816 |
| 240-299 | 266,112 | 0.6931 | 0.3739 | 0.2739 | 0.2718 | 0.959 | 0.899 |

Monthly consistency (log-loss improvement of full vs naive_rw, millinats):

| month | vs naive_rw | vs structural |
|---|---|---|
| 2026-06 | 31.63 | -0.12 |
| 2026-07 | 55.13 | -0.64 |
| 2026-08 | 38.19 | 3.12 |
| 2026-09 | 44.65 | -0.43 |
| 2026-10 | 51.26 | 0.24 |
| 2026-11 | 31.55 | 4.27 |

Reliability of `full` (all elapsed times):

| p bin | n | mean p | observed |
|---|---|---|---|
| 0.0-0.1 | 200,642 | 0.031 | 0.052 |
| 0.1-0.2 | 93,487 | 0.150 | 0.173 |
| 0.2-0.3 | 101,296 | 0.251 | 0.263 |
| 0.3-0.4 | 122,268 | 0.352 | 0.358 |
| 0.4-0.5 | 170,793 | 0.453 | 0.461 |
| 0.5-0.6 | 176,554 | 0.546 | 0.545 |
| 0.6-0.7 | 120,554 | 0.648 | 0.645 |
| 0.7-0.8 | 97,712 | 0.749 | 0.738 |
| 0.8-0.9 | 91,917 | 0.850 | 0.827 |
| 0.9-1.0 | 195,272 | 0.970 | 0.954 |

### Direction from *now*: P(S(t+h) > S(t)) (excl. unchanged, n=1,322,513)

| model | log loss (coin=0.6931) | AUC | accuracy |
|---|---|---|---|
| structural | 0.6860 | 0.5645 | 0.544 |
| full | 0.6861 | 0.5645 | 0.544 |

Information coefficient of the drift forecast: Pearson 0.0613, Spearman 0.0892
Top-decile-confidence directional accuracy: 0.640 (n=132,252)

### Volatility / speed of movement

| metric | naive (5-min RV) | model |
|---|---|---|
| QLIKE vs 5s-sampled realised var | 3.1778 | 1.5113 |
| corr(log forecast var, log realised var) | 0.6884 | 0.7480 |

### Magnitude: predictive quantiles of the log return (n=60,000)

| model | mean pinball (bps) | 50% interval coverage | 90% interval coverage | 90% width (bps) |
|---|---|---|---|---|
| naive_rw | 1.6708 | 0.451 | 0.781 | 12.34 |
| structural | 1.6183 | 0.513 | 0.896 | 17.41 |
| full | 1.6177 | 0.514 | 0.894 | 17.36 |

### Threshold probabilities at the horizon: P(S(t+h) ≥ K·(1+δ))

| δ (bps) | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|
| -20 | 0.964 | 0.1052 | 0.0839 | 0.0837 | 0.944 |
| -10 | 0.875 | 0.2561 | 0.2198 | 0.2197 | 0.910 |
| +10 | 0.124 | 0.2610 | 0.2190 | 0.2189 | 0.909 |
| +20 | 0.038 | 0.1078 | 0.0851 | 0.0850 | 0.943 |

### Touch probabilities: P(price reaches K·(1±δ) before the horizon ends | not there now)

| level | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| K+5bp | 1,145,295 | 0.232 | 0.4544 | 0.4152 | 0.3737 | 0.863 |
| K-5bp | 1,134,969 | 0.237 | 0.4551 | 0.4177 | 0.3762 | 0.864 |
| K+10bp | 1,276,013 | 0.129 | 0.3225 | 0.2732 | 0.2545 | 0.889 |
| K-10bp | 1,273,273 | 0.129 | 0.3125 | 0.2722 | 0.2519 | 0.892 |
| K+20bp | 1,346,632 | 0.043 | 0.1509 | 0.1202 | 0.1122 | 0.925 |
| K-20bp | 1,346,436 | 0.044 | 0.1474 | 0.1174 | 0.1097 | 0.930 |
| K+30bp | 1,362,091 | 0.018 | 0.0754 | 0.0588 | 0.0544 | 0.945 |
| K-30bp | 1,362,802 | 0.018 | 0.0725 | 0.0578 | 0.0530 | 0.948 |

### First passage from the current price: P(+δ first), P(−δ first), P(neither) within the horizon

| δ (bps) | n | P(up first) obs | naive 3-class LL | structural LL | full LL | up-vs-down AUC (decided rows) |
|---|---|---|---|---|---|---|
| 5 | 1,370,444 | 0.240 | 0.9124 | 0.8910 | 0.7509 | 0.573 |
| 10 | 1,370,490 | 0.110 | 0.6178 | 0.5345 | 0.4791 | 0.568 |
| 20 | 1,370,494 | 0.030 | 0.2542 | 0.2020 | 0.1810 | 0.601 |
| 30 | 1,370,495 | 0.011 | 0.1177 | 0.0935 | 0.0799 | 0.660 |

## Horizon 30: 30-second

### P(S(t+h) ≥ K) — above the fixed 5-minute reference (decision times whose horizon stays inside the window)

| model | log loss | Brier | AUC | ECE | accuracy |
|---|---|---|---|---|---|
| climatology | 0.6931 | 0.2500 | 0.5000 | 0.0106 | 0.503 |
| naive_rw | 0.3579 | 0.1069 | 0.9309 | 0.0306 | 0.852 |
| vol_only | 0.3400 | 0.1080 | 0.9318 | 0.0407 | 0.852 |
| structural | 0.3256 | 0.1033 | 0.9343 | 0.0115 | 0.850 |
| full | 0.3161 | 0.0995 | 0.9383 | 0.0025 | 0.858 |
| full+recal | 0.3160 | 0.0995 | 0.9383 | 0.0020 | 0.858 |

log-loss change from causal trailing recalibration (full -> full+recal): 0.059 millinats, 95% CI [-0.056, 0.173]

log-loss improvement of `full` over `naive_rw`: 41.804 millinats/decision, 95% day-block CI [38.013, 46.027]

log-loss improvement of `full` over `structural`: 9.534 millinats/decision, 95% day-block CI [6.818, 12.912]

By elapsed time in the window (log loss; skill = 1 - LL/LL_climatology-at-0.5):

| elapsed s | n | base | naive_rw | structural | full | full AUC | full acc |
|---|---|---|---|---|---|---|---|
| 0-0 | 44,352 | 0.6931 | 0.6932 | 0.6774 | 0.6694 | 0.618 | 0.583 |
| 1-59 | 261,695 | 0.6931 | 0.5030 | 0.4748 | 0.4609 | 0.862 | 0.777 |
| 60-119 | 266,112 | 0.6931 | 0.3668 | 0.3312 | 0.3201 | 0.937 | 0.863 |
| 120-179 | 266,112 | 0.6931 | 0.3033 | 0.2694 | 0.2610 | 0.958 | 0.893 |
| 180-239 | 266,112 | 0.6931 | 0.2551 | 0.2260 | 0.2188 | 0.971 | 0.912 |
| 240-299 | 137,473 | 0.6931 | 0.2609 | 0.2189 | 0.2135 | 0.972 | 0.917 |

Monthly consistency (log-loss improvement of full vs naive_rw, millinats):

| month | vs naive_rw | vs structural |
|---|---|---|
| 2026-06 | 25.22 | 1.38 |
| 2026-07 | 37.76 | 6.79 |
| 2026-08 | 54.78 | 20.87 |
| 2026-09 | 46.04 | 7.93 |
| 2026-10 | 43.82 | 9.76 |
| 2026-11 | 73.24 | 29.13 |

Reliability of `full` (all elapsed times):

| p bin | n | mean p | observed |
|---|---|---|---|
| 0.0-0.1 | 335,657 | 0.029 | 0.027 |
| 0.1-0.2 | 97,027 | 0.146 | 0.137 |
| 0.2-0.3 | 63,293 | 0.247 | 0.243 |
| 0.3-0.4 | 48,384 | 0.349 | 0.347 |
| 0.4-0.5 | 57,917 | 0.454 | 0.448 |
| 0.5-0.6 | 69,658 | 0.549 | 0.547 |
| 0.6-0.7 | 62,020 | 0.650 | 0.650 |
| 0.7-0.8 | 70,255 | 0.752 | 0.751 |
| 0.8-0.9 | 104,469 | 0.854 | 0.856 |
| 0.9-1.0 | 333,176 | 0.971 | 0.970 |

### Direction from *now*: P(S(t+h) > S(t)) (excl. unchanged, n=1,252,770)

| model | log loss (coin=0.6931) | AUC | accuracy |
|---|---|---|---|
| structural | 0.6711 | 0.6171 | 0.583 |
| full | 0.6714 | 0.6166 | 0.583 |

Information coefficient of the drift forecast: Pearson 0.1356, Spearman 0.1861
Top-decile-confidence directional accuracy: 0.714 (n=125,277)

### Volatility / speed of movement

| metric | naive (5-min RV) | model |
|---|---|---|
| QLIKE vs 5s-sampled realised var | 4.2041 | 2.7528 |
| corr(log forecast var, log realised var) | 0.5764 | 0.6257 |

### Magnitude: predictive quantiles of the log return (n=60,000)

| model | mean pinball (bps) | 50% interval coverage | 90% interval coverage | 90% width (bps) |
|---|---|---|---|---|
| naive_rw | 0.7513 | 0.508 | 0.801 | 6.04 |
| structural | 0.7248 | 0.549 | 0.897 | 7.94 |
| full | 0.7241 | 0.541 | 0.894 | 7.91 |

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
| K+5bp | 1,145,295 | 0.076 | 0.2190 | 0.2054 | 0.1689 | 0.916 |
| K-5bp | 1,134,969 | 0.079 | 0.2299 | 0.2143 | 0.1758 | 0.913 |
| K+10bp | 1,276,013 | 0.036 | 0.1106 | 0.0987 | 0.0850 | 0.952 |
| K-10bp | 1,273,273 | 0.037 | 0.1120 | 0.1011 | 0.0864 | 0.952 |
| K+20bp | 1,346,632 | 0.011 | 0.0383 | 0.0325 | 0.0289 | 0.974 |
| K-20bp | 1,346,436 | 0.011 | 0.0365 | 0.0316 | 0.0281 | 0.977 |
| K+30bp | 1,362,091 | 0.005 | 0.0166 | 0.0139 | 0.0126 | 0.975 |
| K-30bp | 1,362,802 | 0.004 | 0.0155 | 0.0132 | 0.0118 | 0.980 |

### First passage from the current price: P(+δ first), P(−δ first), P(neither) within the horizon

| δ (bps) | n | P(up first) obs | naive 3-class LL | structural LL | full LL | up-vs-down AUC (decided rows) |
|---|---|---|---|---|---|---|
| 5 | 1,370,455 | 0.079 | 0.5274 | 0.4869 | 0.4137 | 0.631 |
| 10 | 1,370,487 | 0.018 | 0.1758 | 0.1463 | 0.1272 | 0.642 |
| 20 | 1,370,494 | 0.003 | 0.0352 | 0.0277 | 0.0230 | 0.727 |
| 30 | 1,370,495 | 0.001 | 0.0122 | 0.0098 | 0.0076 | 0.779 |

## Horizon 60: 1-minute

### P(S(t+h) ≥ K) — above the fixed 5-minute reference (decision times whose horizon stays inside the window)

| model | log loss | Brier | AUC | ECE | accuracy |
|---|---|---|---|---|---|
| climatology | 0.6932 | 0.2500 | 0.5000 | 0.0096 | 0.500 |
| naive_rw | 0.4562 | 0.1428 | 0.8790 | 0.0327 | 0.793 |
| vol_only | 0.4351 | 0.1426 | 0.8802 | 0.0352 | 0.793 |
| structural | 0.4251 | 0.1389 | 0.8838 | 0.0091 | 0.793 |
| full | 0.4199 | 0.1367 | 0.8871 | 0.0040 | 0.798 |
| full+recal | 0.4199 | 0.1367 | 0.8871 | 0.0025 | 0.798 |

log-loss change from causal trailing recalibration (full -> full+recal): -0.052 millinats, 95% CI [-0.168, 0.067]

log-loss improvement of `full` over `naive_rw`: 36.331 millinats/decision, 95% day-block CI [33.435, 39.497]

log-loss improvement of `full` over `structural`: 5.235 millinats/decision, 95% day-block CI [3.460, 7.483]

By elapsed time in the window (log loss; skill = 1 - LL/LL_climatology-at-0.5):

| elapsed s | n | base | naive_rw | structural | full | full AUC | full acc |
|---|---|---|---|---|---|---|---|
| 0-0 | 44,352 | 0.6931 | 0.6932 | 0.6837 | 0.6796 | 0.591 | 0.564 |
| 1-59 | 261,695 | 0.6931 | 0.5751 | 0.5524 | 0.5459 | 0.795 | 0.716 |
| 60-119 | 266,112 | 0.6931 | 0.4656 | 0.4307 | 0.4249 | 0.886 | 0.805 |
| 120-179 | 266,112 | 0.6931 | 0.3968 | 0.3617 | 0.3566 | 0.921 | 0.843 |
| 180-239 | 266,112 | 0.6931 | 0.3504 | 0.3160 | 0.3122 | 0.940 | 0.867 |
| 240-299 | 4,417 | 0.6931 | 0.4219 | 0.3523 | 0.3481 | 0.927 | 0.851 |

Monthly consistency (log-loss improvement of full vs naive_rw, millinats):

| month | vs naive_rw | vs structural |
|---|---|---|
| 2026-06 | 23.34 | 0.57 |
| 2026-07 | 32.53 | 3.35 |
| 2026-08 | 45.34 | 13.03 |
| 2026-09 | 41.52 | 3.87 |
| 2026-10 | 38.09 | 4.86 |
| 2026-11 | 54.63 | 14.92 |

Reliability of `full` (all elapsed times):

| p bin | n | mean p | observed |
|---|---|---|---|
| 0.0-0.1 | 194,442 | 0.039 | 0.037 |
| 0.1-0.2 | 104,032 | 0.148 | 0.140 |
| 0.2-0.3 | 84,246 | 0.249 | 0.237 |
| 0.3-0.4 | 72,796 | 0.349 | 0.345 |
| 0.4-0.5 | 85,951 | 0.453 | 0.451 |
| 0.5-0.6 | 97,262 | 0.549 | 0.548 |
| 0.6-0.7 | 85,157 | 0.650 | 0.654 |
| 0.7-0.8 | 90,665 | 0.751 | 0.758 |
| 0.8-0.9 | 104,191 | 0.852 | 0.855 |
| 0.9-1.0 | 190,058 | 0.961 | 0.960 |

### Direction from *now*: P(S(t+h) > S(t)) (excl. unchanged, n=1,311,123)

| model | log loss (coin=0.6931) | AUC | accuracy |
|---|---|---|---|
| structural | 0.6815 | 0.5847 | 0.560 |
| full | 0.6815 | 0.5846 | 0.560 |

Information coefficient of the drift forecast: Pearson 0.0986, Spearman 0.1316
Top-decile-confidence directional accuracy: 0.664 (n=131,113)

### Volatility / speed of movement

| metric | naive (5-min RV) | model |
|---|---|---|
| QLIKE vs 5s-sampled realised var | 3.2012 | 1.5643 |
| corr(log forecast var, log realised var) | 0.6091 | 0.6471 |

### Magnitude: predictive quantiles of the log return (n=60,000)

| model | mean pinball (bps) | 50% interval coverage | 90% interval coverage | 90% width (bps) |
|---|---|---|---|---|
| naive_rw | 1.1067 | 0.451 | 0.778 | 8.54 |
| structural | 1.0677 | 0.522 | 0.899 | 11.76 |
| full | 1.0674 | 0.522 | 0.898 | 11.76 |

### Threshold probabilities at the horizon: P(S(t+h) ≥ K·(1+δ))

| δ (bps) | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|
| -20 | 0.975 | 0.0552 | 0.0449 | 0.0449 | 0.979 |
| -10 | 0.905 | 0.1675 | 0.1405 | 0.1404 | 0.955 |
| +10 | 0.093 | 0.1670 | 0.1381 | 0.1380 | 0.955 |
| +20 | 0.025 | 0.0571 | 0.0453 | 0.0452 | 0.977 |

### Touch probabilities: P(price reaches K·(1±δ) before the horizon ends | not there now)

| level | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| K+5bp | 1,145,295 | 0.129 | 0.3247 | 0.2940 | 0.2587 | 0.886 |
| K-5bp | 1,134,969 | 0.134 | 0.3348 | 0.3018 | 0.2653 | 0.884 |
| K+10bp | 1,276,013 | 0.064 | 0.1838 | 0.1563 | 0.1424 | 0.927 |
| K-10bp | 1,273,273 | 0.065 | 0.1843 | 0.1589 | 0.1440 | 0.928 |
| K+20bp | 1,346,632 | 0.020 | 0.0700 | 0.0572 | 0.0526 | 0.960 |
| K-20bp | 1,346,436 | 0.021 | 0.0677 | 0.0555 | 0.0512 | 0.964 |
| K+30bp | 1,362,091 | 0.008 | 0.0321 | 0.0258 | 0.0237 | 0.969 |
| K-30bp | 1,362,802 | 0.008 | 0.0295 | 0.0242 | 0.0222 | 0.973 |

### First passage from the current price: P(+δ first), P(−δ first), P(neither) within the horizon

| δ (bps) | n | P(up first) obs | naive 3-class LL | structural LL | full LL | up-vs-down AUC (decided rows) |
|---|---|---|---|---|---|---|
| 5 | 1,370,442 | 0.149 | 0.7838 | 0.7353 | 0.6338 | 0.604 |
| 10 | 1,370,487 | 0.046 | 0.3594 | 0.2961 | 0.2661 | 0.612 |
| 20 | 1,370,494 | 0.008 | 0.0907 | 0.0716 | 0.0616 | 0.687 |
| 30 | 1,370,495 | 0.002 | 0.0335 | 0.0266 | 0.0216 | 0.748 |
