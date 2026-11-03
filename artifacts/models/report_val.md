# Out-of-sample report — split `val` ('2026-03-01', '2026-06-01')  (809,850 decision rows, 26,208 five-minute windows)


## Horizon T: 5-minute (to the window close)

### P(S(t+h) ≥ K) — above the fixed 5-minute reference

| model | log loss | Brier | AUC | ECE | accuracy |
|---|---|---|---|---|---|
| climatology | 0.6931 | 0.2500 | 0.5000 | 0.0073 | 0.501 |
| naive_rw | 0.5698 | 0.1783 | 0.8151 | 0.0486 | 0.727 |
| vol_only | 0.5241 | 0.1739 | 0.8174 | 0.0113 | 0.727 |
| structural | 0.5198 | 0.1739 | 0.8188 | 0.0245 | 0.728 |
| full | 0.5189 | 0.1738 | 0.8187 | 0.0234 | 0.728 |
| full+recal | 0.5124 | 0.1731 | 0.8186 | 0.0046 | 0.728 |

log-loss change from causal trailing recalibration (full -> full+recal): 6.524 millinats, 95% CI [4.358, 8.544]

log-loss improvement of `full` over `naive_rw`: 50.916 millinats/decision, 95% day-block CI [42.600, 58.822]

log-loss improvement of `full` over `structural`: 0.850 millinats/decision, 95% day-block CI [0.386, 1.395]

By elapsed time in the window (log loss; skill = 1 - LL/LL_climatology-at-0.5):

| elapsed s | n | base | naive_rw | structural | full | full AUC | full acc |
|---|---|---|---|---|---|---|---|
| 0-0 | 26,208 | 0.6931 | 0.6932 | 0.6920 | 0.6921 | 0.529 | 0.520 |
| 1-59 | 154,650 | 0.6931 | 0.6643 | 0.6562 | 0.6562 | 0.647 | 0.600 |
| 60-119 | 157,248 | 0.6931 | 0.6158 | 0.5935 | 0.5932 | 0.745 | 0.675 |
| 120-179 | 157,248 | 0.6931 | 0.5653 | 0.5274 | 0.5269 | 0.813 | 0.733 |
| 180-239 | 157,248 | 0.6931 | 0.5176 | 0.4539 | 0.4531 | 0.873 | 0.791 |
| 240-299 | 157,248 | 0.6931 | 0.4671 | 0.3413 | 0.3387 | 0.941 | 0.874 |

Monthly consistency (log-loss improvement of full vs naive_rw, millinats):

| month | vs naive_rw | vs structural |
|---|---|---|
| 2026-03 | 45.91 | 1.26 |
| 2026-04 | 44.62 | 0.47 |
| 2026-05 | 62.39 | 0.81 |

Reliability of `full` (all elapsed times):

| p bin | n | mean p | observed |
|---|---|---|---|
| 0.0-0.1 | 111,345 | 0.031 | 0.065 |
| 0.1-0.2 | 53,253 | 0.150 | 0.187 |
| 0.2-0.3 | 60,229 | 0.251 | 0.278 |
| 0.3-0.4 | 73,901 | 0.352 | 0.366 |
| 0.4-0.5 | 103,049 | 0.453 | 0.463 |
| 0.5-0.6 | 107,162 | 0.546 | 0.536 |
| 0.6-0.7 | 74,888 | 0.648 | 0.633 |
| 0.7-0.8 | 60,215 | 0.748 | 0.720 |
| 0.8-0.9 | 55,088 | 0.850 | 0.813 |
| 0.9-1.0 | 110,720 | 0.968 | 0.936 |

### Direction from *now*: P(S(t+h) > S(t)) (excl. unchanged, n=790,877)

| model | log loss (coin=0.6931) | AUC | accuracy |
|---|---|---|---|
| structural | 0.6880 | 0.5546 | 0.536 |
| full | 0.6878 | 0.5558 | 0.537 |

Information coefficient of the drift forecast: Pearson 0.0546, Spearman 0.0771
Top-decile-confidence directional accuracy: 0.622 (n=79,088)

### Volatility / speed of movement

| metric | naive (5-min RV) | model |
|---|---|---|
| QLIKE vs 5s-sampled realised var | 1.8891 | 1.2295 |
| corr(log forecast var, log realised var) | 0.6761 | 0.7332 |

### Magnitude: predictive quantiles of the log return (n=30,000)

| model | mean pinball (bps) | 50% interval coverage | 90% interval coverage | 90% width (bps) |
|---|---|---|---|---|
| naive_rw | 1.8588 | 0.467 | 0.803 | 15.21 |
| structural | 1.8184 | 0.520 | 0.900 | 21.02 |
| full | 1.8165 | 0.520 | 0.897 | 20.89 |

### Threshold probabilities at the horizon: P(S(t+h) ≥ K·(1+δ))

| δ (bps) | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|
| -20 | 0.956 | 0.1185 | 0.1000 | 0.0998 | 0.934 |
| -10 | 0.863 | 0.2761 | 0.2436 | 0.2434 | 0.897 |
| +10 | 0.139 | 0.2723 | 0.2431 | 0.2428 | 0.900 |
| +20 | 0.043 | 0.1145 | 0.0977 | 0.0973 | 0.935 |

### Touch probabilities: P(price reaches K·(1±δ) before the horizon ends | not there now)

| level | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| K+5bp | 658,631 | 0.265 | 0.4738 | 0.4596 | 0.4102 | 0.852 |
| K-5bp | 658,281 | 0.265 | 0.4798 | 0.4640 | 0.4126 | 0.850 |
| K+10bp | 745,164 | 0.152 | 0.3480 | 0.3169 | 0.2902 | 0.877 |
| K-10bp | 743,841 | 0.149 | 0.3519 | 0.3200 | 0.2913 | 0.873 |
| K+20bp | 793,163 | 0.052 | 0.1675 | 0.1443 | 0.1331 | 0.914 |
| K-20bp | 792,574 | 0.053 | 0.1709 | 0.1444 | 0.1331 | 0.916 |
| K+30bp | 804,000 | 0.021 | 0.0876 | 0.0736 | 0.0670 | 0.928 |
| K-30bp | 803,786 | 0.023 | 0.0952 | 0.0753 | 0.0692 | 0.931 |

### First passage from the current price: P(+δ first), P(−δ first), P(neither) within the horizon

| δ (bps) | n | P(up first) obs | naive 3-class LL | structural LL | full LL | up-vs-down AUC (decided rows) |
|---|---|---|---|---|---|---|
| 5 | 809,836 | 0.275 | 0.9725 | 1.0102 | 0.8202 | 0.571 |
| 10 | 809,848 | 0.132 | 0.6995 | 0.6532 | 0.5645 | 0.562 |
| 20 | 809,850 | 0.037 | 0.3110 | 0.2613 | 0.2303 | 0.605 |
| 30 | 809,850 | 0.013 | 0.1486 | 0.1202 | 0.1032 | 0.663 |

## Horizon 30: 30-second

### P(S(t+h) ≥ K) — above the fixed 5-minute reference (decision times whose horizon stays inside the window)

| model | log loss | Brier | AUC | ECE | accuracy |
|---|---|---|---|---|---|
| climatology | 0.6931 | 0.2500 | 0.5000 | 0.0085 | 0.504 |
| naive_rw | 0.3453 | 0.1052 | 0.9322 | 0.0206 | 0.851 |
| vol_only | 0.3353 | 0.1063 | 0.9332 | 0.0363 | 0.851 |
| structural | 0.3225 | 0.1023 | 0.9356 | 0.0095 | 0.852 |
| full | 0.3187 | 0.1008 | 0.9372 | 0.0061 | 0.855 |
| full+recal | 0.3180 | 0.1007 | 0.9373 | 0.0019 | 0.855 |

log-loss change from causal trailing recalibration (full -> full+recal): 0.708 millinats, 95% CI [0.467, 0.907]

log-loss improvement of `full` over `naive_rw`: 26.573 millinats/decision, 95% day-block CI [23.593, 29.823]

log-loss improvement of `full` over `structural`: 3.817 millinats/decision, 95% day-block CI [2.659, 5.197]

By elapsed time in the window (log loss; skill = 1 - LL/LL_climatology-at-0.5):

| elapsed s | n | base | naive_rw | structural | full | full AUC | full acc |
|---|---|---|---|---|---|---|---|
| 0-0 | 26,208 | 0.6931 | 0.6933 | 0.6839 | 0.6799 | 0.589 | 0.564 |
| 1-59 | 154,650 | 0.6931 | 0.4832 | 0.4633 | 0.4578 | 0.864 | 0.780 |
| 60-119 | 157,248 | 0.6931 | 0.3391 | 0.3197 | 0.3156 | 0.939 | 0.864 |
| 120-179 | 157,248 | 0.6931 | 0.2835 | 0.2630 | 0.2595 | 0.959 | 0.892 |
| 180-239 | 157,248 | 0.6931 | 0.2447 | 0.2246 | 0.2220 | 0.970 | 0.909 |
| 240-299 | 81,222 | 0.6931 | 0.2967 | 0.2484 | 0.2453 | 0.964 | 0.904 |

Monthly consistency (log-loss improvement of full vs naive_rw, millinats):

| month | vs naive_rw | vs structural |
|---|---|---|
| 2026-03 | 15.79 | 1.00 |
| 2026-04 | 26.24 | 3.60 |
| 2026-05 | 38.06 | 6.95 |

Reliability of `full` (all elapsed times):

| p bin | n | mean p | observed |
|---|---|---|---|
| 0.0-0.1 | 187,955 | 0.030 | 0.024 |
| 0.1-0.2 | 59,982 | 0.147 | 0.134 |
| 0.2-0.3 | 41,126 | 0.247 | 0.239 |
| 0.3-0.4 | 32,226 | 0.349 | 0.343 |
| 0.4-0.5 | 35,947 | 0.454 | 0.444 |
| 0.5-0.6 | 43,202 | 0.549 | 0.549 |
| 0.6-0.7 | 38,002 | 0.650 | 0.654 |
| 0.7-0.8 | 43,855 | 0.752 | 0.758 |
| 0.8-0.9 | 62,232 | 0.853 | 0.863 |
| 0.9-1.0 | 189,297 | 0.971 | 0.974 |

### Direction from *now*: P(S(t+h) > S(t)) (excl. unchanged, n=760,288)

| model | log loss (coin=0.6931) | AUC | accuracy |
|---|---|---|---|
| structural | 0.6758 | 0.6031 | 0.572 |
| full | 0.6758 | 0.6033 | 0.572 |

Information coefficient of the drift forecast: Pearson 0.1224, Spearman 0.1623
Top-decile-confidence directional accuracy: 0.697 (n=76,029)

### Volatility / speed of movement

| metric | naive (5-min RV) | model |
|---|---|---|
| QLIKE vs 5s-sampled realised var | 2.7347 | 2.1769 |
| corr(log forecast var, log realised var) | 0.5248 | 0.5724 |

### Magnitude: predictive quantiles of the log return (n=30,000)

| model | mean pinball (bps) | 50% interval coverage | 90% interval coverage | 90% width (bps) |
|---|---|---|---|---|
| naive_rw | 0.8475 | 0.497 | 0.816 | 7.42 |
| structural | 0.8213 | 0.535 | 0.907 | 9.51 |
| full | 0.8209 | 0.531 | 0.904 | 9.49 |

### Threshold probabilities at the horizon: P(S(t+h) ≥ K·(1+δ))

| δ (bps) | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|
| -20 | 0.974 | 0.0402 | 0.0338 | 0.0336 | 0.989 |
| -10 | 0.905 | 0.1247 | 0.1073 | 0.1071 | 0.974 |
| +10 | 0.094 | 0.1218 | 0.1059 | 0.1056 | 0.975 |
| +20 | 0.025 | 0.0414 | 0.0341 | 0.0340 | 0.987 |

### Touch probabilities: P(price reaches K·(1±δ) before the horizon ends | not there now)

| level | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| K+5bp | 658,631 | 0.092 | 0.2516 | 0.2446 | 0.1992 | 0.904 |
| K-5bp | 658,281 | 0.092 | 0.2534 | 0.2455 | 0.2002 | 0.903 |
| K+10bp | 745,164 | 0.045 | 0.1341 | 0.1226 | 0.1052 | 0.942 |
| K-10bp | 743,841 | 0.045 | 0.1344 | 0.1226 | 0.1052 | 0.941 |
| K+20bp | 793,163 | 0.014 | 0.0505 | 0.0431 | 0.0383 | 0.965 |
| K-20bp | 792,574 | 0.014 | 0.0472 | 0.0407 | 0.0361 | 0.971 |
| K+30bp | 804,000 | 0.005 | 0.0217 | 0.0184 | 0.0165 | 0.964 |
| K-30bp | 803,786 | 0.006 | 0.0213 | 0.0174 | 0.0156 | 0.977 |

### First passage from the current price: P(+δ first), P(−δ first), P(neither) within the horizon

| δ (bps) | n | P(up first) obs | naive 3-class LL | structural LL | full LL | up-vs-down AUC (decided rows) |
|---|---|---|---|---|---|---|
| 5 | 809,837 | 0.098 | 0.6136 | 0.6033 | 0.4967 | 0.626 |
| 10 | 809,848 | 0.024 | 0.2301 | 0.1943 | 0.1686 | 0.652 |
| 20 | 809,850 | 0.003 | 0.0507 | 0.0401 | 0.0321 | 0.752 |
| 30 | 809,850 | 0.001 | 0.0162 | 0.0133 | 0.0099 | 0.831 |

## Horizon 60: 1-minute

### P(S(t+h) ≥ K) — above the fixed 5-minute reference (decision times whose horizon stays inside the window)

| model | log loss | Brier | AUC | ECE | accuracy |
|---|---|---|---|---|---|
| climatology | 0.6931 | 0.2500 | 0.5000 | 0.0092 | 0.502 |
| naive_rw | 0.4418 | 0.1406 | 0.8815 | 0.0216 | 0.792 |
| vol_only | 0.4300 | 0.1407 | 0.8832 | 0.0340 | 0.792 |
| structural | 0.4212 | 0.1376 | 0.8861 | 0.0109 | 0.795 |
| full | 0.4196 | 0.1369 | 0.8871 | 0.0090 | 0.797 |
| full+recal | 0.4190 | 0.1369 | 0.8870 | 0.0036 | 0.797 |

log-loss change from causal trailing recalibration (full -> full+recal): 0.576 millinats, 95% CI [0.320, 0.781]

log-loss improvement of `full` over `naive_rw`: 22.207 millinats/decision, 95% day-block CI [20.020, 24.684]

log-loss improvement of `full` over `structural`: 1.559 millinats/decision, 95% day-block CI [1.083, 2.174]

By elapsed time in the window (log loss; skill = 1 - LL/LL_climatology-at-0.5):

| elapsed s | n | base | naive_rw | structural | full | full AUC | full acc |
|---|---|---|---|---|---|---|---|
| 0-0 | 26,208 | 0.6931 | 0.6932 | 0.6900 | 0.6874 | 0.562 | 0.546 |
| 1-59 | 154,650 | 0.6931 | 0.5592 | 0.5443 | 0.5424 | 0.797 | 0.718 |
| 60-119 | 157,248 | 0.6931 | 0.4379 | 0.4178 | 0.4165 | 0.891 | 0.807 |
| 120-179 | 157,248 | 0.6931 | 0.3774 | 0.3561 | 0.3547 | 0.922 | 0.841 |
| 180-239 | 157,248 | 0.6931 | 0.3517 | 0.3235 | 0.3222 | 0.936 | 0.861 |
| 240-299 | 2,598 | 0.6931 | 0.5027 | 0.4255 | 0.4238 | 0.894 | 0.812 |

Monthly consistency (log-loss improvement of full vs naive_rw, millinats):

| month | vs naive_rw | vs structural |
|---|---|---|
| 2026-03 | 14.10 | 0.61 |
| 2026-04 | 22.02 | 1.45 |
| 2026-05 | 30.77 | 2.65 |

Reliability of `full` (all elapsed times):

| p bin | n | mean p | observed |
|---|---|---|---|
| 0.0-0.1 | 107,207 | 0.040 | 0.031 |
| 0.1-0.2 | 61,031 | 0.148 | 0.128 |
| 0.2-0.3 | 52,786 | 0.249 | 0.237 |
| 0.3-0.4 | 46,236 | 0.349 | 0.346 |
| 0.4-0.5 | 53,957 | 0.453 | 0.451 |
| 0.5-0.6 | 60,035 | 0.548 | 0.550 |
| 0.6-0.7 | 51,238 | 0.650 | 0.656 |
| 0.7-0.8 | 53,994 | 0.751 | 0.764 |
| 0.8-0.9 | 61,286 | 0.852 | 0.865 |
| 0.9-1.0 | 107,430 | 0.960 | 0.967 |

### Direction from *now*: P(S(t+h) > S(t)) (excl. unchanged, n=789,651)

| model | log loss (coin=0.6931) | AUC | accuracy |
|---|---|---|---|
| structural | 0.6852 | 0.5696 | 0.549 |
| full | 0.6850 | 0.5704 | 0.549 |

Information coefficient of the drift forecast: Pearson 0.0892, Spearman 0.1140
Top-decile-confidence directional accuracy: 0.640 (n=78,966)

### Volatility / speed of movement

| metric | naive (5-min RV) | model |
|---|---|---|
| QLIKE vs 5s-sampled realised var | 1.7440 | 1.1265 |
| corr(log forecast var, log realised var) | 0.5526 | 0.5987 |

### Magnitude: predictive quantiles of the log return (n=30,000)

| model | mean pinball (bps) | 50% interval coverage | 90% interval coverage | 90% width (bps) |
|---|---|---|---|---|
| naive_rw | 1.2289 | 0.463 | 0.804 | 10.50 |
| structural | 1.1959 | 0.531 | 0.913 | 14.09 |
| full | 1.1954 | 0.532 | 0.911 | 14.06 |

### Threshold probabilities at the horizon: P(S(t+h) ≥ K·(1+δ))

| δ (bps) | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|
| -20 | 0.969 | 0.0683 | 0.0556 | 0.0555 | 0.973 |
| -10 | 0.892 | 0.1879 | 0.1617 | 0.1615 | 0.946 |
| +10 | 0.107 | 0.1829 | 0.1595 | 0.1593 | 0.947 |
| +20 | 0.030 | 0.0669 | 0.0547 | 0.0545 | 0.971 |

### Touch probabilities: P(price reaches K·(1±δ) before the horizon ends | not there now)

| level | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| K+5bp | 658,631 | 0.153 | 0.3591 | 0.3404 | 0.2963 | 0.873 |
| K-5bp | 658,281 | 0.153 | 0.3627 | 0.3431 | 0.2986 | 0.870 |
| K+10bp | 745,164 | 0.078 | 0.2130 | 0.1902 | 0.1717 | 0.914 |
| K-10bp | 743,841 | 0.078 | 0.2154 | 0.1910 | 0.1724 | 0.913 |
| K+20bp | 793,163 | 0.025 | 0.0891 | 0.0738 | 0.0675 | 0.948 |
| K-20bp | 792,574 | 0.025 | 0.0871 | 0.0717 | 0.0656 | 0.952 |
| K+30bp | 804,000 | 0.010 | 0.0408 | 0.0340 | 0.0310 | 0.958 |
| K-30bp | 803,786 | 0.010 | 0.0407 | 0.0326 | 0.0299 | 0.965 |

### First passage from the current price: P(+δ first), P(−δ first), P(neither) within the horizon

| δ (bps) | n | P(up first) obs | naive 3-class LL | structural LL | full LL | up-vs-down AUC (decided rows) |
|---|---|---|---|---|---|---|
| 5 | 809,836 | 0.179 | 0.8750 | 0.8778 | 0.7275 | 0.601 |
| 10 | 809,848 | 0.057 | 0.4401 | 0.3813 | 0.3385 | 0.614 |
| 20 | 809,850 | 0.010 | 0.1266 | 0.0999 | 0.0847 | 0.707 |
| 30 | 809,850 | 0.003 | 0.0465 | 0.0369 | 0.0291 | 0.776 |
