# Out-of-sample report — split `val` ('2026-03-01', '2026-06-01')  (809,850 decision rows, 26,208 five-minute windows)


## Horizon 10: 10-second

### P(S(t+h) ≥ K) — above the fixed 5-minute reference (decision times whose horizon stays inside the window)

| model | log loss | Brier | AUC | ECE | accuracy |
|---|---|---|---|---|---|
| climatology | 0.6931 | 0.2500 | 0.5000 | 0.0086 | 0.506 |
| naive_rw | 0.2251 | 0.0645 | 0.9739 | 0.0248 | 0.916 |
| vol_only | 0.2246 | 0.0682 | 0.9742 | 0.0485 | 0.916 |
| structural | 0.2022 | 0.0616 | 0.9752 | 0.0082 | 0.912 |
| full | 0.1928 | 0.0580 | 0.9774 | 0.0043 | 0.920 |
| full+recal | 0.1925 | 0.0580 | 0.9774 | 0.0015 | 0.920 |

log-loss change from causal trailing recalibration (full -> full+recal): 0.298 millinats, 95% CI [0.183, 0.401]

log-loss improvement of `full` over `naive_rw`: 32.302 millinats/decision, 95% day-block CI [28.934, 35.439]

log-loss improvement of `full` over `structural`: 9.372 millinats/decision, 95% day-block CI [7.380, 11.472]

By elapsed time in the window (log loss; skill = 1 - LL/LL_climatology-at-0.5):

| elapsed s | n | base | naive_rw | structural | full | full AUC | full acc |
|---|---|---|---|---|---|---|---|
| 0-0 | 26,208 | 0.6931 | 0.6935 | 0.6780 | 0.6614 | 0.628 | 0.597 |
| 1-59 | 154,650 | 0.6931 | 0.3485 | 0.3232 | 0.3058 | 0.942 | 0.867 |
| 60-119 | 157,248 | 0.6931 | 0.2086 | 0.1898 | 0.1799 | 0.980 | 0.931 |
| 120-179 | 157,248 | 0.6931 | 0.1670 | 0.1490 | 0.1418 | 0.987 | 0.948 |
| 180-239 | 157,248 | 0.6931 | 0.1415 | 0.1249 | 0.1193 | 0.991 | 0.957 |
| 240-299 | 133,638 | 0.6931 | 0.1764 | 0.1368 | 0.1318 | 0.989 | 0.955 |

Monthly consistency (log-loss improvement of full vs naive_rw, millinats):

| month | vs naive_rw | vs structural |
|---|---|---|
| 2026-03 | 20.32 | 3.79 |
| 2026-04 | 32.82 | 8.94 |
| 2026-05 | 44.17 | 15.58 |

Reliability of `full` (all elapsed times):

| p bin | n | mean p | observed |
|---|---|---|---|
| 0.0-0.1 | 287,771 | 0.019 | 0.016 |
| 0.1-0.2 | 38,258 | 0.144 | 0.129 |
| 0.2-0.3 | 20,838 | 0.246 | 0.231 |
| 0.3-0.4 | 15,625 | 0.349 | 0.340 |
| 0.4-0.5 | 17,975 | 0.453 | 0.443 |
| 0.5-0.6 | 24,371 | 0.550 | 0.551 |
| 0.6-0.7 | 22,047 | 0.650 | 0.659 |
| 0.7-0.8 | 25,620 | 0.752 | 0.758 |
| 0.8-0.9 | 41,401 | 0.856 | 0.865 |
| 0.9-1.0 | 292,334 | 0.981 | 0.983 |

### Direction from *now*: P(S(t+h) > S(t)) (excl. unchanged, n=674,669)

| model | log loss (coin=0.6931) | AUC | accuracy |
|---|---|---|---|
| structural | 0.6572 | 0.6506 | 0.608 |
| full | 0.6583 | 0.6499 | 0.608 |

Information coefficient of the drift forecast: Pearson 0.1867, Spearman 0.2580
Top-decile-confidence directional accuracy: 0.760 (n=67,467)

### Volatility / speed of movement

| metric | naive (5-min RV) | model |
|---|---|---|
| QLIKE vs 5s-sampled realised var | 6.6553 | 6.2041 |
| corr(log forecast var, log realised var) | 0.4906 | 0.5435 |

### Magnitude: predictive quantiles of the log return (n=30,000)

| model | mean pinball (bps) | 50% interval coverage | 90% interval coverage | 90% width (bps) |
|---|---|---|---|---|
| naive_rw | 0.4541 | 0.599 | 0.851 | 4.29 |
| structural | 0.4378 | 0.554 | 0.892 | 4.66 |
| full | 0.4370 | 0.540 | 0.888 | 4.63 |

### Threshold probabilities at the horizon: P(S(t+h) ≥ K·(1+δ))

| δ (bps) | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|
| -20 | 0.977 | 0.0197 | 0.0170 | 0.0168 | 0.997 |
| -10 | 0.914 | 0.0645 | 0.0555 | 0.0552 | 0.993 |
| +10 | 0.085 | 0.0636 | 0.0551 | 0.0548 | 0.993 |
| +20 | 0.022 | 0.0201 | 0.0171 | 0.0169 | 0.997 |

### Touch probabilities: P(price reaches K·(1±δ) before the horizon ends | not there now)

| level | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| K+5bp | 658,631 | 0.038 | 0.1397 | 0.1534 | 0.0967 | 0.939 |
| K-5bp | 658,281 | 0.037 | 0.1392 | 0.1533 | 0.0970 | 0.938 |
| K+10bp | 745,164 | 0.018 | 0.0659 | 0.0686 | 0.0472 | 0.966 |
| K-10bp | 743,841 | 0.018 | 0.0650 | 0.0677 | 0.0465 | 0.967 |
| K+20bp | 793,163 | 0.006 | 0.0215 | 0.0207 | 0.0158 | 0.976 |
| K-20bp | 792,574 | 0.006 | 0.0202 | 0.0197 | 0.0148 | 0.984 |
| K+30bp | 804,000 | 0.002 | 0.0087 | 0.0080 | 0.0063 | 0.977 |
| K-30bp | 803,786 | 0.002 | 0.0088 | 0.0080 | 0.0064 | 0.987 |

### First passage from the current price: P(+δ first), P(−δ first), P(neither) within the horizon

| δ (bps) | n | P(up first) obs | naive 3-class LL | structural LL | full LL | up-vs-down AUC (decided rows) |
|---|---|---|---|---|---|---|
| 5 | 809,838 | 0.028 | 0.2619 | 0.2852 | 0.1972 | 0.665 |
| 10 | 809,848 | 0.005 | 0.0669 | 0.0589 | 0.0436 | 0.696 |
| 20 | 809,850 | 0.001 | 0.0104 | 0.0087 | 0.0063 | 0.809 |
| 30 | 809,850 | 0.000 | 0.0024 | 0.0021 | 0.0015 | 0.902 |

## Horizon 15: 15-second

### P(S(t+h) ≥ K) — above the fixed 5-minute reference (decision times whose horizon stays inside the window)

| model | log loss | Brier | AUC | ECE | accuracy |
|---|---|---|---|---|---|
| climatology | 0.6931 | 0.2500 | 0.5000 | 0.0083 | 0.505 |
| naive_rw | 0.2635 | 0.0772 | 0.9627 | 0.0228 | 0.896 |
| vol_only | 0.2572 | 0.0793 | 0.9633 | 0.0398 | 0.896 |
| structural | 0.2406 | 0.0743 | 0.9648 | 0.0088 | 0.894 |
| full | 0.2334 | 0.0715 | 0.9668 | 0.0048 | 0.900 |
| full+recal | 0.2330 | 0.0715 | 0.9669 | 0.0012 | 0.900 |

log-loss change from causal trailing recalibration (full -> full+recal): 0.333 millinats, 95% CI [0.166, 0.476]

log-loss improvement of `full` over `naive_rw`: 30.092 millinats/decision, 95% day-block CI [26.829, 33.502]

log-loss improvement of `full` over `structural`: 7.195 millinats/decision, 95% day-block CI [5.414, 9.121]

By elapsed time in the window (log loss; skill = 1 - LL/LL_climatology-at-0.5):

| elapsed s | n | base | naive_rw | structural | full | full AUC | full acc |
|---|---|---|---|---|---|---|---|
| 0-0 | 26,208 | 0.6931 | 0.6934 | 0.6794 | 0.6708 | 0.610 | 0.581 |
| 1-59 | 154,650 | 0.6931 | 0.3962 | 0.3721 | 0.3597 | 0.920 | 0.838 |
| 60-119 | 157,248 | 0.6931 | 0.2542 | 0.2342 | 0.2261 | 0.969 | 0.909 |
| 120-179 | 157,248 | 0.6931 | 0.2021 | 0.1844 | 0.1783 | 0.980 | 0.931 |
| 180-239 | 157,248 | 0.6931 | 0.1728 | 0.1559 | 0.1512 | 0.986 | 0.943 |
| 240-299 | 120,543 | 0.6931 | 0.2099 | 0.1684 | 0.1645 | 0.983 | 0.941 |

Monthly consistency (log-loss improvement of full vs naive_rw, millinats):

| month | vs naive_rw | vs structural |
|---|---|---|
| 2026-03 | 17.87 | 2.52 |
| 2026-04 | 30.16 | 6.80 |
| 2026-05 | 42.65 | 12.42 |

Reliability of `full` (all elapsed times):

| p bin | n | mean p | observed |
|---|---|---|---|
| 0.0-0.1 | 256,892 | 0.022 | 0.019 |
| 0.1-0.2 | 46,620 | 0.144 | 0.133 |
| 0.2-0.3 | 27,272 | 0.246 | 0.230 |
| 0.3-0.4 | 20,289 | 0.349 | 0.333 |
| 0.4-0.5 | 23,414 | 0.454 | 0.446 |
| 0.5-0.6 | 29,966 | 0.550 | 0.550 |
| 0.6-0.7 | 28,520 | 0.650 | 0.655 |
| 0.7-0.8 | 30,787 | 0.752 | 0.762 |
| 0.8-0.9 | 49,526 | 0.856 | 0.865 |
| 0.9-1.0 | 259,859 | 0.977 | 0.980 |

### Direction from *now*: P(S(t+h) > S(t)) (excl. unchanged, n=711,480)

| model | log loss (coin=0.6931) | AUC | accuracy |
|---|---|---|---|
| structural | 0.6637 | 0.6358 | 0.596 |
| full | 0.6643 | 0.6353 | 0.597 |

Information coefficient of the drift forecast: Pearson 0.1617, Spearman 0.2223
Top-decile-confidence directional accuracy: 0.740 (n=71,148)

### Volatility / speed of movement

| metric | naive (5-min RV) | model |
|---|---|---|
| QLIKE vs 5s-sampled realised var | 4.7806 | 4.2521 |
| corr(log forecast var, log realised var) | 0.5077 | 0.5558 |

### Magnitude: predictive quantiles of the log return (n=30,000)

| model | mean pinball (bps) | 50% interval coverage | 90% interval coverage | 90% width (bps) |
|---|---|---|---|---|
| naive_rw | 0.5741 | 0.556 | 0.838 | 5.25 |
| structural | 0.5544 | 0.548 | 0.899 | 6.12 |
| full | 0.5537 | 0.533 | 0.895 | 6.08 |

### Threshold probabilities at the horizon: P(S(t+h) ≥ K·(1+δ))

| δ (bps) | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|
| -20 | 0.976 | 0.0255 | 0.0217 | 0.0216 | 0.995 |
| -10 | 0.912 | 0.0823 | 0.0709 | 0.0708 | 0.988 |
| +10 | 0.087 | 0.0809 | 0.0702 | 0.0700 | 0.988 |
| +20 | 0.023 | 0.0267 | 0.0220 | 0.0219 | 0.994 |

### Touch probabilities: P(price reaches K·(1±δ) before the horizon ends | not there now)

| level | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| K+5bp | 658,631 | 0.053 | 0.1740 | 0.1747 | 0.1282 | 0.928 |
| K-5bp | 658,281 | 0.053 | 0.1745 | 0.1752 | 0.1288 | 0.927 |
| K+10bp | 745,164 | 0.025 | 0.0851 | 0.0812 | 0.0640 | 0.959 |
| K-10bp | 743,841 | 0.025 | 0.0846 | 0.0807 | 0.0634 | 0.960 |
| K+20bp | 793,163 | 0.008 | 0.0294 | 0.0264 | 0.0222 | 0.972 |
| K-20bp | 792,574 | 0.008 | 0.0274 | 0.0249 | 0.0207 | 0.978 |
| K+30bp | 804,000 | 0.003 | 0.0123 | 0.0108 | 0.0093 | 0.965 |
| K-30bp | 803,786 | 0.003 | 0.0122 | 0.0104 | 0.0089 | 0.981 |

### First passage from the current price: P(+δ first), P(−δ first), P(neither) within the horizon

| δ (bps) | n | P(up first) obs | naive 3-class LL | structural LL | full LL | up-vs-down AUC (decided rows) |
|---|---|---|---|---|---|---|
| 5 | 809,837 | 0.046 | 0.3713 | 0.3634 | 0.2889 | 0.650 |
| 10 | 809,848 | 0.009 | 0.1086 | 0.0912 | 0.0742 | 0.679 |
| 20 | 809,850 | 0.001 | 0.0188 | 0.0155 | 0.0115 | 0.786 |
| 30 | 809,850 | 0.000 | 0.0052 | 0.0045 | 0.0033 | 0.864 |
