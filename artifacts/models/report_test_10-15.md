# Out-of-sample report — split `test` ('2026-06-01', '2026-11-03')  (1,370,495 decision rows, 44,352 five-minute windows)


## Horizon 10: 10-second

### P(S(t+h) ≥ K) — above the fixed 5-minute reference (decision times whose horizon stays inside the window)

| model | log loss | Brier | AUC | ECE | accuracy |
|---|---|---|---|---|---|
| climatology | 0.6931 | 0.2500 | 0.5000 | 0.0112 | 0.507 |
| naive_rw | 0.2332 | 0.0667 | 0.9733 | 0.0321 | 0.916 |
| vol_only | 0.2297 | 0.0704 | 0.9736 | 0.0530 | 0.916 |
| structural | 0.2067 | 0.0636 | 0.9741 | 0.0138 | 0.907 |
| full | 0.1898 | 0.0571 | 0.9780 | 0.0019 | 0.920 |
| full+recal | 0.1898 | 0.0571 | 0.9780 | 0.0012 | 0.920 |

log-loss change from causal trailing recalibration (full -> full+recal): 0.029 millinats, 95% CI [-0.036, 0.100]

log-loss improvement of `full` over `naive_rw`: 43.394 millinats/decision, 95% day-block CI [39.474, 47.726]

log-loss improvement of `full` over `structural`: 16.945 millinats/decision, 95% day-block CI [13.504, 21.019]

By elapsed time in the window (log loss; skill = 1 - LL/LL_climatology-at-0.5):

| elapsed s | n | base | naive_rw | structural | full | full AUC | full acc |
|---|---|---|---|---|---|---|---|
| 0-0 | 44,352 | 0.6931 | 0.6932 | 0.6709 | 0.6476 | 0.655 | 0.615 |
| 1-59 | 261,695 | 0.6931 | 0.3725 | 0.3434 | 0.3121 | 0.940 | 0.861 |
| 60-119 | 266,112 | 0.6931 | 0.2268 | 0.1994 | 0.1802 | 0.980 | 0.930 |
| 120-179 | 266,112 | 0.6931 | 0.1787 | 0.1538 | 0.1406 | 0.988 | 0.947 |
| 180-239 | 266,112 | 0.6931 | 0.1477 | 0.1273 | 0.1164 | 0.991 | 0.957 |
| 240-299 | 226,177 | 0.6931 | 0.1539 | 0.1218 | 0.1140 | 0.991 | 0.961 |

Monthly consistency (log-loss improvement of full vs naive_rw, millinats):

| month | vs naive_rw | vs structural |
|---|---|---|
| 2026-06 | 25.46 | 4.71 |
| 2026-07 | 42.60 | 13.98 |
| 2026-08 | 56.87 | 30.72 |
| 2026-09 | 47.28 | 15.82 |
| 2026-10 | 43.28 | 18.25 |
| 2026-11 | 75.57 | 42.35 |

Reliability of `full` (all elapsed times):

| p bin | n | mean p | observed |
|---|---|---|---|
| 0.0-0.1 | 499,213 | 0.018 | 0.016 |
| 0.1-0.2 | 57,546 | 0.143 | 0.135 |
| 0.2-0.3 | 29,403 | 0.246 | 0.239 |
| 0.3-0.4 | 23,509 | 0.350 | 0.347 |
| 0.4-0.5 | 31,384 | 0.454 | 0.452 |
| 0.5-0.6 | 43,343 | 0.550 | 0.546 |
| 0.6-0.7 | 36,936 | 0.649 | 0.647 |
| 0.7-0.8 | 39,004 | 0.752 | 0.757 |
| 0.8-0.9 | 64,347 | 0.857 | 0.857 |
| 0.9-1.0 | 505,875 | 0.981 | 0.981 |

### Direction from *now*: P(S(t+h) > S(t)) (excl. unchanged, n=1,104,619)

| model | log loss (coin=0.6931) | AUC | accuracy |
|---|---|---|---|
| structural | 0.6529 | 0.6605 | 0.616 |
| full | 0.6558 | 0.6576 | 0.616 |

Information coefficient of the drift forecast: Pearson 0.2053, Spearman 0.2912
Top-decile-confidence directional accuracy: 0.767 (n=110,462)

### Volatility / speed of movement

| metric | naive (5-min RV) | model |
|---|---|---|
| QLIKE vs 5s-sampled realised var | 8.1746 | 6.9080 |
| corr(log forecast var, log realised var) | 0.5107 | 0.5718 |

### Magnitude: predictive quantiles of the log return (n=60,000)

| model | mean pinball (bps) | 50% interval coverage | 90% interval coverage | 90% width (bps) |
|---|---|---|---|---|
| naive_rw | 0.3870 | 0.627 | 0.848 | 3.49 |
| structural | 0.3717 | 0.588 | 0.891 | 3.87 |
| full | 0.3703 | 0.565 | 0.886 | 3.80 |

### Threshold probabilities at the horizon: P(S(t+h) ≥ K·(1+δ))

| δ (bps) | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|
| -20 | 0.981 | 0.0162 | 0.0141 | 0.0140 | 0.998 |
| -10 | 0.925 | 0.0544 | 0.0466 | 0.0464 | 0.994 |
| +10 | 0.073 | 0.0535 | 0.0453 | 0.0451 | 0.994 |
| +20 | 0.019 | 0.0162 | 0.0137 | 0.0136 | 0.998 |

### Touch probabilities: P(price reaches K·(1±δ) before the horizon ends | not there now)

| level | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| K+5bp | 1,145,295 | 0.030 | 0.1149 | 0.1242 | 0.0789 | 0.948 |
| K-5bp | 1,134,969 | 0.031 | 0.1221 | 0.1311 | 0.0830 | 0.945 |
| K+10bp | 1,276,013 | 0.014 | 0.0514 | 0.0535 | 0.0368 | 0.973 |
| K-10bp | 1,273,273 | 0.014 | 0.0527 | 0.0558 | 0.0376 | 0.973 |
| K+20bp | 1,346,632 | 0.004 | 0.0161 | 0.0157 | 0.0118 | 0.984 |
| K-20bp | 1,346,436 | 0.005 | 0.0159 | 0.0157 | 0.0118 | 0.986 |
| K+30bp | 1,362,091 | 0.002 | 0.0067 | 0.0062 | 0.0050 | 0.981 |
| K-30bp | 1,362,802 | 0.002 | 0.0065 | 0.0063 | 0.0049 | 0.985 |

### First passage from the current price: P(+δ first), P(−δ first), P(neither) within the horizon

| δ (bps) | n | P(up first) obs | naive 3-class LL | structural LL | full LL | up-vs-down AUC (decided rows) |
|---|---|---|---|---|---|---|
| 5 | 1,370,465 | 0.022 | 0.2100 | 0.2169 | 0.1544 | 0.671 |
| 10 | 1,370,489 | 0.004 | 0.0457 | 0.0424 | 0.0311 | 0.678 |
| 20 | 1,370,495 | 0.000 | 0.0081 | 0.0066 | 0.0049 | 0.758 |
| 30 | 1,370,495 | 0.000 | 0.0025 | 0.0020 | 0.0016 | 0.764 |

## Horizon 15: 15-second

### P(S(t+h) ≥ K) — above the fixed 5-minute reference (decision times whose horizon stays inside the window)

| model | log loss | Brier | AUC | ECE | accuracy |
|---|---|---|---|---|---|
| climatology | 0.6931 | 0.2500 | 0.5000 | 0.0110 | 0.505 |
| naive_rw | 0.2741 | 0.0792 | 0.9619 | 0.0316 | 0.897 |
| vol_only | 0.2631 | 0.0815 | 0.9623 | 0.0456 | 0.897 |
| structural | 0.2450 | 0.0761 | 0.9635 | 0.0133 | 0.890 |
| full | 0.2307 | 0.0705 | 0.9675 | 0.0024 | 0.901 |
| full+recal | 0.2307 | 0.0705 | 0.9675 | 0.0018 | 0.901 |

log-loss change from causal trailing recalibration (full -> full+recal): -0.003 millinats, 95% CI [-0.083, 0.082]

log-loss improvement of `full` over `naive_rw`: 43.410 millinats/decision, 95% day-block CI [39.480, 47.740]

log-loss improvement of `full` over `structural`: 14.256 millinats/decision, 95% day-block CI [11.019, 18.160]

By elapsed time in the window (log loss; skill = 1 - LL/LL_climatology-at-0.5):

| elapsed s | n | base | naive_rw | structural | full | full AUC | full acc |
|---|---|---|---|---|---|---|---|
| 0-0 | 44,352 | 0.6931 | 0.6932 | 0.6726 | 0.6594 | 0.638 | 0.600 |
| 1-59 | 261,695 | 0.6931 | 0.4198 | 0.3905 | 0.3657 | 0.916 | 0.833 |
| 60-119 | 266,112 | 0.6931 | 0.2733 | 0.2426 | 0.2260 | 0.969 | 0.910 |
| 120-179 | 266,112 | 0.6931 | 0.2210 | 0.1912 | 0.1795 | 0.980 | 0.931 |
| 180-239 | 266,112 | 0.6931 | 0.1829 | 0.1593 | 0.1495 | 0.986 | 0.943 |
| 240-299 | 204,212 | 0.6931 | 0.1855 | 0.1505 | 0.1433 | 0.987 | 0.949 |

Monthly consistency (log-loss improvement of full vs naive_rw, millinats):

| month | vs naive_rw | vs structural |
|---|---|---|
| 2026-06 | 25.71 | 3.09 |
| 2026-07 | 42.02 | 11.43 |
| 2026-08 | 56.81 | 27.27 |
| 2026-09 | 47.53 | 13.00 |
| 2026-10 | 43.40 | 15.29 |
| 2026-11 | 78.65 | 38.55 |

Reliability of `full` (all elapsed times):

| p bin | n | mean p | observed |
|---|---|---|---|
| 0.0-0.1 | 448,863 | 0.021 | 0.020 |
| 0.1-0.2 | 72,643 | 0.144 | 0.137 |
| 0.2-0.3 | 39,928 | 0.246 | 0.238 |
| 0.3-0.4 | 30,430 | 0.350 | 0.347 |
| 0.4-0.5 | 38,481 | 0.454 | 0.445 |
| 0.5-0.6 | 51,345 | 0.550 | 0.545 |
| 0.6-0.7 | 46,373 | 0.649 | 0.646 |
| 0.7-0.8 | 48,844 | 0.752 | 0.756 |
| 0.8-0.9 | 81,584 | 0.857 | 0.860 |
| 0.9-1.0 | 450,104 | 0.978 | 0.978 |

### Direction from *now*: P(S(t+h) > S(t)) (excl. unchanged, n=1,166,098)

| model | log loss (coin=0.6931) | AUC | accuracy |
|---|---|---|---|
| structural | 0.6590 | 0.6467 | 0.606 |
| full | 0.6612 | 0.6443 | 0.606 |

Information coefficient of the drift forecast: Pearson 0.1782, Spearman 0.2508
Top-decile-confidence directional accuracy: 0.748 (n=116,610)

### Volatility / speed of movement

| metric | naive (5-min RV) | model |
|---|---|---|
| QLIKE vs 5s-sampled realised var | 6.2233 | 4.9369 |
| corr(log forecast var, log realised var) | 0.5379 | 0.5921 |

### Magnitude: predictive quantiles of the log return (n=60,000)

| model | mean pinball (bps) | 50% interval coverage | 90% interval coverage | 90% width (bps) |
|---|---|---|---|---|
| naive_rw | 0.4967 | 0.578 | 0.830 | 4.27 |
| structural | 0.4786 | 0.576 | 0.894 | 5.08 |
| full | 0.4772 | 0.552 | 0.888 | 5.02 |

### Threshold probabilities at the horizon: P(S(t+h) ≥ K·(1+δ))

| δ (bps) | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|
| -20 | 0.981 | 0.0212 | 0.0181 | 0.0180 | 0.996 |
| -10 | 0.923 | 0.0706 | 0.0602 | 0.0601 | 0.991 |
| +10 | 0.075 | 0.0692 | 0.0585 | 0.0584 | 0.991 |
| +20 | 0.019 | 0.0211 | 0.0176 | 0.0176 | 0.996 |

### Touch probabilities: P(price reaches K·(1±δ) before the horizon ends | not there now)

| level | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| K+5bp | 1,145,295 | 0.043 | 0.1465 | 0.1439 | 0.1060 | 0.938 |
| K-5bp | 1,134,969 | 0.045 | 0.1543 | 0.1517 | 0.1113 | 0.935 |
| K+10bp | 1,276,013 | 0.020 | 0.0675 | 0.0642 | 0.0505 | 0.967 |
| K-10bp | 1,273,273 | 0.020 | 0.0691 | 0.0664 | 0.0515 | 0.967 |
| K+20bp | 1,346,632 | 0.006 | 0.0218 | 0.0196 | 0.0165 | 0.981 |
| K-20bp | 1,346,436 | 0.006 | 0.0213 | 0.0195 | 0.0163 | 0.982 |
| K+30bp | 1,362,091 | 0.003 | 0.0093 | 0.0081 | 0.0071 | 0.977 |
| K-30bp | 1,362,802 | 0.002 | 0.0087 | 0.0079 | 0.0067 | 0.981 |

### First passage from the current price: P(+δ first), P(−δ first), P(neither) within the horizon

| δ (bps) | n | P(up first) obs | naive 3-class LL | structural LL | full LL | up-vs-down AUC (decided rows) |
|---|---|---|---|---|---|---|
| 5 | 1,370,462 | 0.037 | 0.3069 | 0.2845 | 0.2318 | 0.656 |
| 10 | 1,370,489 | 0.007 | 0.0768 | 0.0663 | 0.0539 | 0.665 |
| 20 | 1,370,495 | 0.001 | 0.0140 | 0.0112 | 0.0087 | 0.734 |
| 30 | 1,370,495 | 0.000 | 0.0045 | 0.0037 | 0.0029 | 0.759 |
