# Out-of-sample report — split `test` ('2025-05-01', '2025-09-01')  (1,085,644 decision rows, 35,136 five-minute windows)


## Horizon T: 5-minute (to the window close)

### P(S(t+h) ≥ K) — above the fixed 5-minute reference

| model | log loss | Brier | AUC | ECE | accuracy |
|---|---|---|---|---|---|
| climatology | 0.6931 | 0.2500 | 0.5000 | 0.0077 | 0.502 |
| naive_rw | 0.4714 | 0.1540 | 0.8591 | 0.0258 | 0.764 |
| vol_only | 0.4563 | 0.1530 | 0.8604 | 0.0250 | 0.764 |
| structural | 0.4504 | 0.1510 | 0.8626 | 0.0043 | 0.766 |
| full | 0.4505 | 0.1510 | 0.8625 | 0.0045 | 0.766 |
| full+recal | 0.4507 | 0.1511 | 0.8624 | 0.0034 | 0.766 |

log-loss change from causal trailing recalibration (full -> full+recal): -0.149 millinats, 95% CI [-0.389, 0.066]

log-loss improvement of `full` over `naive_rw`: 20.892 millinats/decision, 95% day-block CI [19.048, 23.016]

log-loss improvement of `full` over `structural`: -0.093 millinats/decision, 95% day-block CI [-0.218, 0.039]

By elapsed time in the window (log loss; skill = 1 - LL/LL_climatology-at-0.5):

| elapsed s | n | base | naive_rw | structural | full | full AUC | full acc |
|---|---|---|---|---|---|---|---|
| 0-0 | 35,136 | 0.6931 | 0.6932 | 0.6903 | 0.6904 | 0.542 | 0.533 |
| 1-59 | 207,244 | 0.6931 | 0.6561 | 0.6484 | 0.6485 | 0.665 | 0.614 |
| 60-119 | 210,816 | 0.6931 | 0.5876 | 0.5680 | 0.5680 | 0.774 | 0.702 |
| 120-179 | 210,816 | 0.6931 | 0.4967 | 0.4698 | 0.4700 | 0.857 | 0.776 |
| 180-239 | 210,816 | 0.6931 | 0.3831 | 0.3528 | 0.3530 | 0.923 | 0.843 |
| 240-299 | 210,816 | 0.6931 | 0.1998 | 0.1765 | 0.1766 | 0.981 | 0.929 |

Monthly consistency (log-loss improvement of full vs naive_rw, millinats):

| month | vs naive_rw | vs structural |
|---|---|---|
| 2025-05 | 20.56 | 0.15 |
| 2025-06 | 17.51 | -0.26 |
| 2025-07 | 22.62 | -0.22 |
| 2025-08 | 22.83 | -0.05 |

Reliability of `full` (all elapsed times):

| p bin | n | mean p | observed |
|---|---|---|---|
| 0.0-0.1 | 161,480 | 0.032 | 0.028 |
| 0.1-0.2 | 74,695 | 0.149 | 0.145 |
| 0.2-0.3 | 75,454 | 0.251 | 0.241 |
| 0.3-0.4 | 88,121 | 0.352 | 0.338 |
| 0.4-0.5 | 135,691 | 0.455 | 0.450 |
| 0.5-0.6 | 138,972 | 0.545 | 0.548 |
| 0.6-0.7 | 90,898 | 0.648 | 0.654 |
| 0.7-0.8 | 76,708 | 0.749 | 0.750 |
| 0.8-0.9 | 74,216 | 0.851 | 0.850 |
| 0.9-1.0 | 169,409 | 0.969 | 0.968 |

### Direction from *now*: P(S(t+h) > S(t)) (excl. unchanged, n=1,041,029)

| model | log loss (coin=0.6931) | AUC | accuracy |
|---|---|---|---|
| structural | 0.6850 | 0.5694 | 0.547 |
| full | 0.6854 | 0.5684 | 0.547 |

Information coefficient of the drift forecast: Pearson 0.0746, Spearman 0.0978
Top-decile-confidence directional accuracy: 0.647 (n=104,103)

### Volatility / speed of movement

| metric | naive (5-min RV) | model |
|---|---|---|
| QLIKE vs 5s-sampled realised var | 3.3520 | 1.6170 |
| corr(log forecast var, log realised var) | 0.6716 | 0.7370 |

### Magnitude: predictive quantiles of the log return (n=30,000)

| model | mean pinball (bps) | 50% interval coverage | 90% interval coverage | 90% width (bps) |
|---|---|---|---|---|
| naive_rw | 1.5063 | 0.447 | 0.778 | 11.51 |
| structural | 1.4528 | 0.506 | 0.890 | 16.18 |
| full | 1.4526 | 0.506 | 0.889 | 16.11 |

### Threshold probabilities at the horizon: P(S(t+h) ≥ K·(1+δ))

| δ (bps) | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|
| -20 | 0.972 | 0.0895 | 0.0696 | 0.0695 | 0.944 |
| -10 | 0.886 | 0.2592 | 0.2129 | 0.2129 | 0.904 |
| +10 | 0.117 | 0.2609 | 0.2136 | 0.2136 | 0.907 |
| +20 | 0.029 | 0.0903 | 0.0699 | 0.0698 | 0.944 |

### Touch probabilities: P(price reaches K·(1±δ) before the horizon ends | not there now)

| level | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| K+5bp | 909,036 | 0.233 | 0.4771 | 0.4234 | 0.3864 | 0.853 |
| K-5bp | 911,731 | 0.238 | 0.4846 | 0.4217 | 0.3901 | 0.852 |
| K+10bp | 1,018,070 | 0.118 | 0.3174 | 0.2647 | 0.2463 | 0.883 |
| K-10bp | 1,020,601 | 0.121 | 0.3233 | 0.2661 | 0.2506 | 0.883 |
| K+20bp | 1,072,104 | 0.032 | 0.1183 | 0.0956 | 0.0888 | 0.930 |
| K-20bp | 1,072,441 | 0.034 | 0.1289 | 0.1001 | 0.0937 | 0.926 |
| K+30bp | 1,081,806 | 0.011 | 0.0488 | 0.0387 | 0.0360 | 0.952 |
| K-30bp | 1,082,045 | 0.012 | 0.0552 | 0.0426 | 0.0397 | 0.949 |

### First passage from the current price: P(+δ first), P(−δ first), P(neither) within the horizon

| δ (bps) | n | P(up first) obs | naive 3-class LL | structural LL | full LL | up-vs-down AUC (decided rows) |
|---|---|---|---|---|---|---|
| 5 | 1,085,635 | 0.226 | 0.9264 | 0.8810 | 0.7568 | 0.583 |
| 10 | 1,085,644 | 0.092 | 0.5982 | 0.4977 | 0.4541 | 0.576 |
| 20 | 1,085,644 | 0.020 | 0.2051 | 0.1582 | 0.1435 | 0.597 |
| 30 | 1,085,644 | 0.006 | 0.0776 | 0.0600 | 0.0522 | 0.634 |

## Horizon 30: 30-second

### P(S(t+h) ≥ K) — above the fixed 5-minute reference (decision times whose horizon stays inside the window)

| model | log loss | Brier | AUC | ECE | accuracy |
|---|---|---|---|---|---|
| climatology | 0.6929 | 0.2499 | 0.5000 | 0.0084 | 0.510 |
| naive_rw | 0.3461 | 0.1038 | 0.9350 | 0.0323 | 0.857 |
| vol_only | 0.3314 | 0.1053 | 0.9355 | 0.0440 | 0.857 |
| structural | 0.3166 | 0.1004 | 0.9381 | 0.0136 | 0.854 |
| full | 0.3085 | 0.0970 | 0.9413 | 0.0058 | 0.862 |
| full+recal | 0.3083 | 0.0969 | 0.9413 | 0.0032 | 0.862 |

log-loss change from causal trailing recalibration (full -> full+recal): 0.131 millinats, 95% CI [0.030, 0.234]

log-loss improvement of `full` over `naive_rw`: 37.624 millinats/decision, 95% day-block CI [34.879, 40.898]

log-loss improvement of `full` over `structural`: 8.142 millinats/decision, 95% day-block CI [6.416, 10.695]

By elapsed time in the window (log loss; skill = 1 - LL/LL_climatology-at-0.5):

| elapsed s | n | base | naive_rw | structural | full | full AUC | full acc |
|---|---|---|---|---|---|---|---|
| 0-0 | 35,136 | 0.6931 | 0.6932 | 0.6747 | 0.6669 | 0.618 | 0.586 |
| 1-59 | 207,244 | 0.6931 | 0.4930 | 0.4671 | 0.4536 | 0.867 | 0.783 |
| 60-119 | 210,816 | 0.6931 | 0.3605 | 0.3263 | 0.3180 | 0.938 | 0.865 |
| 120-179 | 210,816 | 0.6931 | 0.2891 | 0.2591 | 0.2521 | 0.961 | 0.898 |
| 180-239 | 210,816 | 0.6931 | 0.2522 | 0.2216 | 0.2160 | 0.971 | 0.914 |
| 240-299 | 108,980 | 0.6931 | 0.2188 | 0.1914 | 0.1866 | 0.979 | 0.927 |

Monthly consistency (log-loss improvement of full vs naive_rw, millinats):

| month | vs naive_rw | vs structural |
|---|---|---|
| 2025-05 | 33.73 | 4.71 |
| 2025-06 | 39.70 | 10.02 |
| 2025-07 | 37.94 | 12.26 |
| 2025-08 | 39.26 | 5.55 |

Reliability of `full` (all elapsed times):

| p bin | n | mean p | observed |
|---|---|---|---|
| 0.0-0.1 | 261,419 | 0.029 | 0.026 |
| 0.1-0.2 | 75,457 | 0.145 | 0.136 |
| 0.2-0.3 | 48,074 | 0.247 | 0.233 |
| 0.3-0.4 | 38,896 | 0.350 | 0.334 |
| 0.4-0.5 | 48,420 | 0.453 | 0.447 |
| 0.5-0.6 | 54,493 | 0.550 | 0.557 |
| 0.6-0.7 | 50,769 | 0.650 | 0.669 |
| 0.7-0.8 | 56,361 | 0.751 | 0.767 |
| 0.8-0.9 | 78,112 | 0.854 | 0.860 |
| 0.9-1.0 | 271,807 | 0.972 | 0.972 |

### Direction from *now*: P(S(t+h) > S(t)) (excl. unchanged, n=977,650)

| model | log loss (coin=0.6931) | AUC | accuracy |
|---|---|---|---|
| structural | 0.6699 | 0.6205 | 0.586 |
| full | 0.6701 | 0.6201 | 0.586 |

Information coefficient of the drift forecast: Pearson 0.1638, Spearman 0.2035
Top-decile-confidence directional accuracy: 0.718 (n=97,765)

### Volatility / speed of movement

| metric | naive (5-min RV) | model |
|---|---|---|
| QLIKE vs 5s-sampled realised var | 4.9464 | 3.1700 |
| corr(log forecast var, log realised var) | 0.5141 | 0.5529 |

### Magnitude: predictive quantiles of the log return (n=30,000)

| model | mean pinball (bps) | 50% interval coverage | 90% interval coverage | 90% width (bps) |
|---|---|---|---|---|
| naive_rw | 0.6854 | 0.493 | 0.792 | 5.64 |
| structural | 0.6613 | 0.545 | 0.896 | 7.48 |
| full | 0.6607 | 0.537 | 0.893 | 7.42 |

### Threshold probabilities at the horizon: P(S(t+h) ≥ K·(1+δ))

| δ (bps) | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|
| -20 | 0.985 | 0.0259 | 0.0212 | 0.0211 | 0.992 |
| -10 | 0.929 | 0.1022 | 0.0840 | 0.0838 | 0.979 |
| +10 | 0.074 | 0.0994 | 0.0825 | 0.0824 | 0.981 |
| +20 | 0.015 | 0.0245 | 0.0204 | 0.0203 | 0.992 |

### Touch probabilities: P(price reaches K·(1±δ) before the horizon ends | not there now)

| level | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| K+5bp | 909,036 | 0.073 | 0.2209 | 0.2061 | 0.1675 | 0.913 |
| K-5bp | 911,731 | 0.074 | 0.2274 | 0.2103 | 0.1718 | 0.911 |
| K+10bp | 1,018,070 | 0.031 | 0.0996 | 0.0901 | 0.0762 | 0.954 |
| K-10bp | 1,020,601 | 0.032 | 0.1044 | 0.0930 | 0.0789 | 0.953 |
| K+20bp | 1,072,104 | 0.008 | 0.0262 | 0.0236 | 0.0206 | 0.978 |
| K-20bp | 1,072,441 | 0.008 | 0.0276 | 0.0241 | 0.0211 | 0.980 |
| K+30bp | 1,081,806 | 0.003 | 0.0089 | 0.0079 | 0.0069 | 0.978 |
| K-30bp | 1,082,045 | 0.003 | 0.0100 | 0.0085 | 0.0075 | 0.986 |

### First passage from the current price: P(+δ first), P(−δ first), P(neither) within the horizon

| δ (bps) | n | P(up first) obs | naive 3-class LL | structural LL | full LL | up-vs-down AUC (decided rows) |
|---|---|---|---|---|---|---|
| 5 | 1,085,638 | 0.063 | 0.4760 | 0.4367 | 0.3696 | 0.663 |
| 10 | 1,085,644 | 0.011 | 0.1319 | 0.1062 | 0.0922 | 0.674 |
| 20 | 1,085,644 | 0.001 | 0.0187 | 0.0148 | 0.0123 | 0.704 |
| 30 | 1,085,644 | 0.000 | 0.0041 | 0.0034 | 0.0029 | 0.730 |

## Horizon 60: 1-minute

### P(S(t+h) ≥ K) — above the fixed 5-minute reference (decision times whose horizon stays inside the window)

| model | log loss | Brier | AUC | ECE | accuracy |
|---|---|---|---|---|---|
| climatology | 0.6931 | 0.2500 | 0.5000 | 0.0076 | 0.507 |
| naive_rw | 0.4475 | 0.1398 | 0.8839 | 0.0328 | 0.797 |
| vol_only | 0.4281 | 0.1400 | 0.8848 | 0.0368 | 0.797 |
| structural | 0.4179 | 0.1362 | 0.8882 | 0.0093 | 0.798 |
| full | 0.4148 | 0.1349 | 0.8901 | 0.0075 | 0.802 |
| full+recal | 0.4147 | 0.1348 | 0.8901 | 0.0041 | 0.802 |

log-loss change from causal trailing recalibration (full -> full+recal): 0.114 millinats, 95% CI [-0.051, 0.251]

log-loss improvement of `full` over `naive_rw`: 32.687 millinats/decision, 95% day-block CI [30.371, 34.921]

log-loss improvement of `full` over `structural`: 3.072 millinats/decision, 95% day-block CI [2.131, 4.392]

By elapsed time in the window (log loss; skill = 1 - LL/LL_climatology-at-0.5):

| elapsed s | n | base | naive_rw | structural | full | full AUC | full acc |
|---|---|---|---|---|---|---|---|
| 0-0 | 35,136 | 0.6931 | 0.6932 | 0.6828 | 0.6804 | 0.585 | 0.561 |
| 1-59 | 207,244 | 0.6931 | 0.5696 | 0.5485 | 0.5443 | 0.796 | 0.718 |
| 60-119 | 210,816 | 0.6931 | 0.4589 | 0.4257 | 0.4228 | 0.887 | 0.807 |
| 120-179 | 210,816 | 0.6931 | 0.3845 | 0.3514 | 0.3484 | 0.925 | 0.849 |
| 180-239 | 210,816 | 0.6931 | 0.3403 | 0.3063 | 0.3038 | 0.943 | 0.871 |
| 240-299 | 3,572 | 0.6931 | 0.3150 | 0.2823 | 0.2803 | 0.952 | 0.879 |

Monthly consistency (log-loss improvement of full vs naive_rw, millinats):

| month | vs naive_rw | vs structural |
|---|---|---|
| 2025-05 | 29.35 | 1.69 |
| 2025-06 | 33.82 | 3.61 |
| 2025-07 | 30.60 | 4.97 |
| 2025-08 | 37.15 | 2.00 |

Reliability of `full` (all elapsed times):

| p bin | n | mean p | observed |
|---|---|---|---|
| 0.0-0.1 | 152,445 | 0.038 | 0.037 |
| 0.1-0.2 | 78,878 | 0.148 | 0.137 |
| 0.2-0.3 | 65,243 | 0.248 | 0.233 |
| 0.3-0.4 | 56,218 | 0.350 | 0.334 |
| 0.4-0.5 | 70,567 | 0.454 | 0.447 |
| 0.5-0.6 | 82,042 | 0.548 | 0.556 |
| 0.6-0.7 | 66,238 | 0.650 | 0.665 |
| 0.7-0.8 | 68,305 | 0.751 | 0.765 |
| 0.8-0.9 | 81,607 | 0.852 | 0.858 |
| 0.9-1.0 | 156,857 | 0.963 | 0.963 |

### Direction from *now*: P(S(t+h) > S(t)) (excl. unchanged, n=1,033,560)

| model | log loss (coin=0.6931) | AUC | accuracy |
|---|---|---|---|
| structural | 0.6812 | 0.5862 | 0.561 |
| full | 0.6812 | 0.5861 | 0.561 |

Information coefficient of the drift forecast: Pearson 0.1170, Spearman 0.1432
Top-decile-confidence directional accuracy: 0.662 (n=103,356)

### Volatility / speed of movement

| metric | naive (5-min RV) | model |
|---|---|---|
| QLIKE vs 5s-sampled realised var | 3.4949 | 1.6807 |
| corr(log forecast var, log realised var) | 0.5359 | 0.5642 |

### Magnitude: predictive quantiles of the log return (n=30,000)

| model | mean pinball (bps) | 50% interval coverage | 90% interval coverage | 90% width (bps) |
|---|---|---|---|---|
| naive_rw | 1.0186 | 0.441 | 0.766 | 7.97 |
| structural | 0.9815 | 0.516 | 0.894 | 11.06 |
| full | 0.9810 | 0.516 | 0.890 | 11.01 |

### Threshold probabilities at the horizon: P(S(t+h) ≥ K·(1+δ))

| δ (bps) | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|
| -20 | 0.982 | 0.0447 | 0.0355 | 0.0354 | 0.979 |
| -10 | 0.918 | 0.1603 | 0.1302 | 0.1301 | 0.954 |
| +10 | 0.085 | 0.1579 | 0.1290 | 0.1289 | 0.957 |
| +20 | 0.019 | 0.0423 | 0.0342 | 0.0340 | 0.981 |

### Touch probabilities: P(price reaches K·(1±δ) before the horizon ends | not there now)

| level | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| K+5bp | 909,036 | 0.126 | 0.3324 | 0.2969 | 0.2608 | 0.880 |
| K-5bp | 911,731 | 0.129 | 0.3421 | 0.3011 | 0.2663 | 0.878 |
| K+10bp | 1,018,070 | 0.057 | 0.1716 | 0.1461 | 0.1316 | 0.927 |
| K-10bp | 1,020,601 | 0.058 | 0.1778 | 0.1502 | 0.1357 | 0.925 |
| K+20bp | 1,072,104 | 0.014 | 0.0498 | 0.0423 | 0.0384 | 0.966 |
| K-20bp | 1,072,441 | 0.015 | 0.0542 | 0.0446 | 0.0407 | 0.965 |
| K+30bp | 1,081,806 | 0.005 | 0.0179 | 0.0152 | 0.0138 | 0.973 |
| K-30bp | 1,082,045 | 0.005 | 0.0203 | 0.0165 | 0.0151 | 0.975 |

### First passage from the current price: P(+δ first), P(−δ first), P(neither) within the horizon

| δ (bps) | n | P(up first) obs | naive 3-class LL | structural LL | full LL | up-vs-down AUC (decided rows) |
|---|---|---|---|---|---|---|
| 5 | 1,085,637 | 0.130 | 0.7697 | 0.7143 | 0.6154 | 0.625 |
| 10 | 1,085,644 | 0.032 | 0.3034 | 0.2453 | 0.2201 | 0.631 |
| 20 | 1,085,644 | 0.004 | 0.0574 | 0.0448 | 0.0383 | 0.664 |
| 30 | 1,085,644 | 0.001 | 0.0143 | 0.0118 | 0.0097 | 0.706 |
