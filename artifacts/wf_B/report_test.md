# Out-of-sample report — split `test` ('2025-11-01', '2026-03-01')  (1,058,986 decision rows, 34,272 five-minute windows)


## Horizon T: 5-minute (to the window close)

### P(S(t+h) ≥ K) — above the fixed 5-minute reference

| model | log loss | Brier | AUC | ECE | accuracy |
|---|---|---|---|---|---|
| climatology | 0.6931 | 0.2500 | 0.5000 | 0.0104 | 0.502 |
| naive_rw | 0.4799 | 0.1582 | 0.8501 | 0.0202 | 0.756 |
| vol_only | 0.4699 | 0.1576 | 0.8516 | 0.0255 | 0.756 |
| structural | 0.4644 | 0.1560 | 0.8529 | 0.0045 | 0.756 |
| full | 0.4643 | 0.1560 | 0.8529 | 0.0052 | 0.756 |
| full+recal | 0.4641 | 0.1561 | 0.8527 | 0.0022 | 0.756 |

log-loss change from causal trailing recalibration (full -> full+recal): 0.166 millinats, 95% CI [-0.355, 0.737]

log-loss improvement of `full` over `naive_rw`: 15.612 millinats/decision, 95% day-block CI [12.804, 18.445]

log-loss improvement of `full` over `structural`: 0.139 millinats/decision, 95% day-block CI [-0.165, 0.496]

By elapsed time in the window (log loss; skill = 1 - LL/LL_climatology-at-0.5):

| elapsed s | n | base | naive_rw | structural | full | full AUC | full acc |
|---|---|---|---|---|---|---|---|
| 0-0 | 34,272 | 0.6931 | 0.6931 | 0.6924 | 0.6925 | 0.527 | 0.516 |
| 1-59 | 202,186 | 0.6931 | 0.6559 | 0.6507 | 0.6510 | 0.658 | 0.610 |
| 60-119 | 205,632 | 0.6931 | 0.5863 | 0.5745 | 0.5746 | 0.766 | 0.694 |
| 120-179 | 205,632 | 0.6931 | 0.5019 | 0.4851 | 0.4850 | 0.845 | 0.762 |
| 180-239 | 205,632 | 0.6931 | 0.3911 | 0.3704 | 0.3700 | 0.915 | 0.833 |
| 240-299 | 205,632 | 0.6931 | 0.2316 | 0.2065 | 0.2058 | 0.974 | 0.918 |

Monthly consistency (log-loss improvement of full vs naive_rw, millinats):

| month | vs naive_rw | vs structural |
|---|---|---|
| 2025-11 | 8.25 | -0.16 |
| 2025-12 | 13.79 | -0.14 |
| 2026-01 | 21.75 | 0.90 |
| 2026-02 | 18.84 | -0.09 |

Reliability of `full` (all elapsed times):

| p bin | n | mean p | observed |
|---|---|---|---|
| 0.0-0.1 | 144,903 | 0.031 | 0.029 |
| 0.1-0.2 | 69,795 | 0.150 | 0.138 |
| 0.2-0.3 | 75,007 | 0.251 | 0.237 |
| 0.3-0.4 | 92,076 | 0.352 | 0.342 |
| 0.4-0.5 | 129,469 | 0.454 | 0.449 |
| 0.5-0.6 | 148,401 | 0.546 | 0.544 |
| 0.6-0.7 | 98,546 | 0.647 | 0.649 |
| 0.7-0.8 | 77,652 | 0.749 | 0.746 |
| 0.8-0.9 | 72,129 | 0.850 | 0.855 |
| 0.9-1.0 | 151,008 | 0.969 | 0.969 |

### Direction from *now*: P(S(t+h) > S(t)) (excl. unchanged, n=1,027,027)

| model | log loss (coin=0.6931) | AUC | accuracy |
|---|---|---|---|
| structural | 0.6885 | 0.5490 | 0.532 |
| full | 0.6885 | 0.5495 | 0.532 |

Information coefficient of the drift forecast: Pearson 0.0382, Spearman 0.0625
Top-decile-confidence directional accuracy: 0.622 (n=102,703)

### Volatility / speed of movement

| metric | naive (5-min RV) | model |
|---|---|---|
| QLIKE vs 5s-sampled realised var | 3.1292 | 1.3022 |
| corr(log forecast var, log realised var) | 0.7168 | 0.7671 |

### Magnitude: predictive quantiles of the log return (n=30,000)

| model | mean pinball (bps) | 50% interval coverage | 90% interval coverage | 90% width (bps) |
|---|---|---|---|---|
| naive_rw | 2.1739 | 0.485 | 0.825 | 18.22 |
| structural | 2.1403 | 0.531 | 0.908 | 24.06 |
| full | 2.1401 | 0.531 | 0.908 | 24.07 |

### Threshold probabilities at the horizon: P(S(t+h) ≥ K·(1+δ))

| δ (bps) | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|
| -20 | 0.931 | 0.1524 | 0.1359 | 0.1359 | 0.934 |
| -10 | 0.821 | 0.3101 | 0.2800 | 0.2800 | 0.899 |
| +10 | 0.172 | 0.2956 | 0.2725 | 0.2725 | 0.900 |
| +20 | 0.065 | 0.1462 | 0.1314 | 0.1314 | 0.934 |

### Touch probabilities: P(price reaches K·(1±δ) before the horizon ends | not there now)

| level | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| K+5bp | 833,203 | 0.280 | 0.4676 | 0.4509 | 0.4062 | 0.862 |
| K-5bp | 833,258 | 0.281 | 0.4793 | 0.4547 | 0.4132 | 0.857 |
| K+10bp | 946,849 | 0.179 | 0.3549 | 0.3350 | 0.3094 | 0.883 |
| K-10bp | 943,547 | 0.182 | 0.3715 | 0.3394 | 0.3167 | 0.879 |
| K+20bp | 1,022,976 | 0.076 | 0.1954 | 0.1766 | 0.1646 | 0.919 |
| K-20bp | 1,021,670 | 0.079 | 0.2049 | 0.1823 | 0.1712 | 0.915 |
| K+30bp | 1,044,545 | 0.035 | 0.1057 | 0.0956 | 0.0890 | 0.942 |
| K-30bp | 1,043,950 | 0.039 | 0.1172 | 0.1017 | 0.0961 | 0.940 |

### First passage from the current price: P(+δ first), P(−δ first), P(neither) within the horizon

| δ (bps) | n | P(up first) obs | naive 3-class LL | structural LL | full LL | up-vs-down AUC (decided rows) |
|---|---|---|---|---|---|---|
| 5 | 1,058,914 | 0.296 | 0.9116 | 0.9631 | 0.7902 | 0.559 |
| 10 | 1,058,974 | 0.163 | 0.7132 | 0.6953 | 0.6092 | 0.547 |
| 20 | 1,058,986 | 0.057 | 0.3678 | 0.3331 | 0.3002 | 0.562 |
| 30 | 1,058,986 | 0.023 | 0.1901 | 0.1689 | 0.1513 | 0.589 |

## Horizon 30: 30-second

### P(S(t+h) ≥ K) — above the fixed 5-minute reference (decision times whose horizon stays inside the window)

| model | log loss | Brier | AUC | ECE | accuracy |
|---|---|---|---|---|---|
| climatology | 0.6930 | 0.2499 | 0.5000 | 0.0084 | 0.510 |
| naive_rw | 0.3490 | 0.1075 | 0.9299 | 0.0234 | 0.849 |
| vol_only | 0.3396 | 0.1086 | 0.9307 | 0.0383 | 0.849 |
| structural | 0.3297 | 0.1052 | 0.9323 | 0.0116 | 0.846 |
| full | 0.3233 | 0.1027 | 0.9350 | 0.0061 | 0.852 |
| full+recal | 0.3231 | 0.1027 | 0.9350 | 0.0016 | 0.852 |

log-loss change from causal trailing recalibration (full -> full+recal): 0.283 millinats, 95% CI [0.148, 0.413]

log-loss improvement of `full` over `naive_rw`: 25.672 millinats/decision, 95% day-block CI [22.156, 30.118]

log-loss improvement of `full` over `structural`: 6.345 millinats/decision, 95% day-block CI [4.013, 9.287]

By elapsed time in the window (log loss; skill = 1 - LL/LL_climatology-at-0.5):

| elapsed s | n | base | naive_rw | structural | full | full AUC | full acc |
|---|---|---|---|---|---|---|---|
| 0-0 | 34,272 | 0.6931 | 0.6932 | 0.6898 | 0.6824 | 0.569 | 0.552 |
| 1-59 | 202,186 | 0.6931 | 0.4927 | 0.4750 | 0.4655 | 0.859 | 0.775 |
| 60-119 | 205,632 | 0.6931 | 0.3632 | 0.3412 | 0.3341 | 0.931 | 0.854 |
| 120-179 | 205,632 | 0.6931 | 0.2974 | 0.2768 | 0.2712 | 0.955 | 0.886 |
| 180-239 | 205,632 | 0.6931 | 0.2500 | 0.2310 | 0.2266 | 0.969 | 0.907 |
| 240-299 | 106,262 | 0.6931 | 0.2287 | 0.2082 | 0.2044 | 0.975 | 0.918 |

Monthly consistency (log-loss improvement of full vs naive_rw, millinats):

| month | vs naive_rw | vs structural |
|---|---|---|
| 2025-11 | 19.20 | 1.46 |
| 2025-12 | 30.42 | 9.42 |
| 2026-01 | 39.81 | 12.46 |
| 2026-02 | 11.17 | 1.23 |

Reliability of `full` (all elapsed times):

| p bin | n | mean p | observed |
|---|---|---|---|
| 0.0-0.1 | 241,342 | 0.029 | 0.025 |
| 0.1-0.2 | 73,461 | 0.146 | 0.135 |
| 0.2-0.3 | 52,692 | 0.248 | 0.238 |
| 0.3-0.4 | 43,913 | 0.349 | 0.343 |
| 0.4-0.5 | 49,756 | 0.454 | 0.457 |
| 0.5-0.6 | 58,990 | 0.548 | 0.554 |
| 0.6-0.7 | 52,027 | 0.650 | 0.657 |
| 0.7-0.8 | 60,694 | 0.752 | 0.766 |
| 0.8-0.9 | 80,630 | 0.853 | 0.865 |
| 0.9-1.0 | 246,111 | 0.971 | 0.974 |

### Direction from *now*: P(S(t+h) > S(t)) (excl. unchanged, n=991,241)

| model | log loss (coin=0.6931) | AUC | accuracy |
|---|---|---|---|
| structural | 0.6815 | 0.5816 | 0.556 |
| full | 0.6818 | 0.5815 | 0.555 |

Information coefficient of the drift forecast: Pearson 0.0944, Spearman 0.1267
Top-decile-confidence directional accuracy: 0.675 (n=99,125)

### Volatility / speed of movement

| metric | naive (5-min RV) | model |
|---|---|---|
| QLIKE vs 5s-sampled realised var | 4.0728 | 2.1923 |
| corr(log forecast var, log realised var) | 0.6200 | 0.6469 |

### Magnitude: predictive quantiles of the log return (n=30,000)

| model | mean pinball (bps) | 50% interval coverage | 90% interval coverage | 90% width (bps) |
|---|---|---|---|---|
| naive_rw | 1.0178 | 0.504 | 0.825 | 9.03 |
| structural | 0.9987 | 0.532 | 0.907 | 11.26 |
| full | 0.9982 | 0.524 | 0.904 | 11.21 |

### Threshold probabilities at the horizon: P(S(t+h) ≥ K·(1+δ))

| δ (bps) | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|
| -20 | 0.958 | 0.0564 | 0.0507 | 0.0505 | 0.987 |
| -10 | 0.874 | 0.1470 | 0.1320 | 0.1319 | 0.972 |
| +10 | 0.122 | 0.1454 | 0.1313 | 0.1311 | 0.972 |
| +20 | 0.041 | 0.0564 | 0.0506 | 0.0505 | 0.987 |

### Touch probabilities: P(price reaches K·(1±δ) before the horizon ends | not there now)

| level | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| K+5bp | 833,203 | 0.107 | 0.2583 | 0.2571 | 0.2152 | 0.908 |
| K-5bp | 833,258 | 0.106 | 0.2644 | 0.2599 | 0.2169 | 0.904 |
| K+10bp | 946,849 | 0.059 | 0.1499 | 0.1440 | 0.1259 | 0.941 |
| K-10bp | 943,547 | 0.059 | 0.1528 | 0.1449 | 0.1274 | 0.940 |
| K+20bp | 1,022,976 | 0.022 | 0.0599 | 0.0554 | 0.0502 | 0.972 |
| K-20bp | 1,021,670 | 0.023 | 0.0630 | 0.0579 | 0.0523 | 0.970 |
| K+30bp | 1,044,545 | 0.010 | 0.0282 | 0.0256 | 0.0236 | 0.982 |
| K-30bp | 1,043,950 | 0.010 | 0.0290 | 0.0264 | 0.0242 | 0.981 |

### First passage from the current price: P(+δ first), P(−δ first), P(neither) within the horizon

| δ (bps) | n | P(up first) obs | naive 3-class LL | structural LL | full LL | up-vs-down AUC (decided rows) |
|---|---|---|---|---|---|---|
| 5 | 1,058,916 | 0.137 | 0.6773 | 0.7137 | 0.5870 | 0.597 |
| 10 | 1,058,976 | 0.042 | 0.2975 | 0.2802 | 0.2460 | 0.599 |
| 20 | 1,058,986 | 0.007 | 0.0722 | 0.0632 | 0.0554 | 0.635 |
| 30 | 1,058,986 | 0.002 | 0.0247 | 0.0207 | 0.0177 | 0.677 |

## Horizon 60: 1-minute

### P(S(t+h) ≥ K) — above the fixed 5-minute reference (decision times whose horizon stays inside the window)

| model | log loss | Brier | AUC | ECE | accuracy |
|---|---|---|---|---|---|
| climatology | 0.6931 | 0.2500 | 0.5000 | 0.0085 | 0.507 |
| naive_rw | 0.4449 | 0.1424 | 0.8787 | 0.0230 | 0.790 |
| vol_only | 0.4348 | 0.1427 | 0.8801 | 0.0374 | 0.790 |
| structural | 0.4275 | 0.1401 | 0.8819 | 0.0133 | 0.789 |
| full | 0.4243 | 0.1389 | 0.8838 | 0.0081 | 0.793 |
| full+recal | 0.4239 | 0.1388 | 0.8838 | 0.0022 | 0.793 |

log-loss change from causal trailing recalibration (full -> full+recal): 0.351 millinats, 95% CI [0.154, 0.529]

log-loss improvement of `full` over `naive_rw`: 20.604 millinats/decision, 95% day-block CI [17.928, 23.909]

log-loss improvement of `full` over `structural`: 3.245 millinats/decision, 95% day-block CI [2.040, 4.850]

By elapsed time in the window (log loss; skill = 1 - LL/LL_climatology-at-0.5):

| elapsed s | n | base | naive_rw | structural | full | full AUC | full acc |
|---|---|---|---|---|---|---|---|
| 0-0 | 34,272 | 0.6931 | 0.6932 | 0.6927 | 0.6893 | 0.546 | 0.530 |
| 1-59 | 202,186 | 0.6931 | 0.5676 | 0.5550 | 0.5512 | 0.789 | 0.712 |
| 60-119 | 205,632 | 0.6931 | 0.4560 | 0.4357 | 0.4321 | 0.881 | 0.797 |
| 120-179 | 205,632 | 0.6931 | 0.3855 | 0.3659 | 0.3629 | 0.918 | 0.838 |
| 180-239 | 205,632 | 0.6931 | 0.3327 | 0.3134 | 0.3109 | 0.941 | 0.866 |
| 240-299 | 3,446 | 0.6931 | 0.3469 | 0.3158 | 0.3114 | 0.940 | 0.859 |

Monthly consistency (log-loss improvement of full vs naive_rw, millinats):

| month | vs naive_rw | vs structural |
|---|---|---|
| 2025-11 | 17.22 | 0.74 |
| 2025-12 | 23.51 | 4.44 |
| 2026-01 | 31.11 | 6.41 |
| 2026-02 | 8.96 | 1.04 |

Reliability of `full` (all elapsed times):

| p bin | n | mean p | observed |
|---|---|---|---|
| 0.0-0.1 | 136,338 | 0.039 | 0.032 |
| 0.1-0.2 | 77,829 | 0.148 | 0.133 |
| 0.2-0.3 | 65,912 | 0.249 | 0.236 |
| 0.3-0.4 | 61,209 | 0.350 | 0.344 |
| 0.4-0.5 | 73,651 | 0.454 | 0.458 |
| 0.5-0.6 | 79,956 | 0.548 | 0.552 |
| 0.6-0.7 | 68,582 | 0.651 | 0.658 |
| 0.7-0.8 | 72,191 | 0.750 | 0.762 |
| 0.8-0.9 | 80,335 | 0.851 | 0.862 |
| 0.9-1.0 | 140,797 | 0.961 | 0.966 |

### Direction from *now*: P(S(t+h) > S(t)) (excl. unchanged, n=1,024,776)

| model | log loss (coin=0.6931) | AUC | accuracy |
|---|---|---|---|
| structural | 0.6874 | 0.5564 | 0.538 |
| full | 0.6875 | 0.5574 | 0.539 |

Information coefficient of the drift forecast: Pearson 0.0649, Spearman 0.0866
Top-decile-confidence directional accuracy: 0.628 (n=102,478)

### Volatility / speed of movement

| metric | naive (5-min RV) | model |
|---|---|---|
| QLIKE vs 5s-sampled realised var | 3.2308 | 1.2319 |
| corr(log forecast var, log realised var) | 0.6461 | 0.6632 |

### Magnitude: predictive quantiles of the log return (n=30,000)

| model | mean pinball (bps) | 50% interval coverage | 90% interval coverage | 90% width (bps) |
|---|---|---|---|---|
| naive_rw | 1.4624 | 0.471 | 0.815 | 12.78 |
| structural | 1.4399 | 0.536 | 0.915 | 16.90 |
| full | 1.4375 | 0.531 | 0.907 | 16.53 |

### Threshold probabilities at the horizon: P(S(t+h) ≥ K·(1+δ))

| δ (bps) | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|
| -20 | 0.951 | 0.0895 | 0.0796 | 0.0792 | 0.971 |
| -10 | 0.859 | 0.2139 | 0.1921 | 0.1918 | 0.944 |
| +10 | 0.136 | 0.2092 | 0.1898 | 0.1893 | 0.944 |
| +20 | 0.047 | 0.0882 | 0.0788 | 0.0783 | 0.970 |

### Touch probabilities: P(price reaches K·(1±δ) before the horizon ends | not there now)

| level | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| K+5bp | 833,203 | 0.171 | 0.3587 | 0.3523 | 0.3084 | 0.879 |
| K-5bp | 833,258 | 0.169 | 0.3702 | 0.3568 | 0.3125 | 0.873 |
| K+10bp | 946,849 | 0.099 | 0.2303 | 0.2182 | 0.1974 | 0.914 |
| K-10bp | 943,547 | 0.099 | 0.2376 | 0.2201 | 0.2004 | 0.911 |
| K+20bp | 1,022,976 | 0.038 | 0.1026 | 0.0931 | 0.0862 | 0.954 |
| K-20bp | 1,021,670 | 0.040 | 0.1076 | 0.0967 | 0.0896 | 0.952 |
| K+30bp | 1,044,545 | 0.017 | 0.0507 | 0.0453 | 0.0422 | 0.970 |
| K-30bp | 1,043,950 | 0.018 | 0.0528 | 0.0469 | 0.0437 | 0.969 |

### First passage from the current price: P(+δ first), P(−δ first), P(neither) within the horizon

| δ (bps) | n | P(up first) obs | naive 3-class LL | structural LL | full LL | up-vs-down AUC (decided rows) |
|---|---|---|---|---|---|---|
| 5 | 1,058,914 | 0.221 | 0.8764 | 0.9395 | 0.7660 | 0.578 |
| 10 | 1,058,974 | 0.087 | 0.5112 | 0.4934 | 0.4320 | 0.577 |
| 20 | 1,058,986 | 0.020 | 0.1680 | 0.1503 | 0.1333 | 0.606 |
| 30 | 1,058,986 | 0.006 | 0.0647 | 0.0561 | 0.0493 | 0.640 |
