# REPORT — BTC movement relative to the fixed 5-minute reference

**Bottom line.** These are results on the held-out test period 2026-06-01 → 2026-11-03 (1,370,495 decision rows). It was never used during development. All numbers below are generated from `artifacts/*/report_*.json`.

* **10-second** — P(price ≥ K): log loss **0.190** vs **0.233** for the naive random walk, an improvement of +43.4 [+39.5, +47.7] millinats per decision. AUC 0.978, accuracy 92.0%, ECE 0.0012. Direction from now: AUC 0.658, top-10%-confidence accuracy 76.7%.
* **15-second** — P(price ≥ K): log loss **0.231** vs **0.274** for the naive random walk, an improvement of +43.4 [+39.5, +47.7] millinats per decision. AUC 0.967, accuracy 90.1%, ECE 0.0018. Direction from now: AUC 0.644, top-10%-confidence accuracy 74.8%.
* **30-second** — P(price ≥ K): log loss **0.316** vs **0.358** for the naive random walk, an improvement of +41.5 [+37.8, +45.7] millinats per decision. AUC 0.938, accuracy 85.8%, ECE 0.0021. Direction from now: AUC 0.616, top-10%-confidence accuracy 71.2%.
* **1-minute** — P(price ≥ K): log loss **0.420** vs **0.456** for the naive random walk, an improvement of +36.1 [+33.3, +39.3] millinats per decision. AUC 0.887, accuracy 79.8%, ECE 0.0027. Direction from now: AUC 0.585, top-10%-confidence accuracy 66.3%.
* **5-minute (to close)** — P(price ≥ K): log loss **0.487** vs **0.534** for the naive random walk, an improvement of +43.7 [+38.1, +49.8] millinats per decision. AUC 0.838, accuracy 74.4%, ECE 0.0025. Direction from now: AUC 0.562, top-10%-confidence accuracy 63.7%.
* With the adaptive prior/head ensemble that ships in the live engine, the 5-minute log loss is **0.4865**.
* Through the 5-minute window, accuracy rises from 52.0% at the open (pure direction) to 89.8% in the last minute.

How to read the numbers. Late in the window most of `P(close ≥ K)` is "physics": the displacement from K measured in units of remaining volatility. Every model gets the easy part right, so the honest comparison is against strong baselines, not a coin flip. The genuinely predictive part lives in three places, each measured separately below:
1. a much better volatility forecast;
2. a short-horizon drift driven mainly by the perpetual→spot lead-lag;
3. learned corrections of the shape, touches and first passages.

# Out-of-sample results

Main test period **2026-06-01 → 2026-11-03** (1,370,495 decision rows). Nothing in this period was used for training, early stopping, feature selection, recalibration choices or hyper-parameters. Log loss is in nats; lower is better. Improvements are reported in **millinats per decision**, with **95% day-block bootstrap CIs** in brackets. A coin flip scores 0.6931.

For calibration, `full+recal` adds the causal trailing recalibration. It is fitted each day on the previous 14 days of resolved outcomes. Enabling it was decided on the validation period.

## 1. P(price ≥ fixed 5-minute reference) — every horizon

| horizon | naive RW | structural | full | full+recal | Δ full vs naive | Δ full vs structural | AUC | accuracy | ECE (full+recal) |
|---|---|---|---|---|---|---|---|---|---|
| 10-second | 0.2332 | 0.2067 | 0.1898 | 0.1898 | +43.4 [+39.5, +47.7] | +16.9 [+13.5, +21.0] | 0.978 | 0.920 | 0.0012 |
| 15-second | 0.2741 | 0.2450 | 0.2307 | 0.2307 | +43.4 [+39.5, +47.7] | +14.3 [+11.0, +18.2] | 0.967 | 0.901 | 0.0018 |
| 30-second | 0.3579 | 0.3257 | 0.3164 | 0.3163 | +41.5 [+37.8, +45.7] | +9.4 [+6.7, +12.8] | 0.938 | 0.858 | 0.0021 |
| 1-minute | 0.4562 | 0.4253 | 0.4201 | 0.4202 | +36.1 [+33.3, +39.3] | +5.2 [+3.5, +7.4] | 0.887 | 0.798 | 0.0027 |
| 5-minute (to close) | 0.5337 | 0.4902 | 0.4900 | 0.4875 | +43.7 [+38.1, +49.8] | +0.1 [-0.5, +0.9] | 0.838 | 0.744 | 0.0025 |

*naive RW* is a driftless Gaussian random walk using the last 5 minutes' realised volatility, which is what most dashboards compute. *structural* is the analytic layer on top of the learned volatility, drift and shape. *full* adds the prior-boosted head. For 30s and 60s the table uses decision times whose horizon ends inside the window.

### Adaptive prior/head ensemble (regime-adaptive weighting)

Each UTC day and elapsed-time bucket, a logistic stack of logit(boosted head) and logit(structural prior) is refitted on the previous 14 days of resolved outcomes. Where the ML correction stops helping, for example at the window open or after a regime shift, weight moves back to the analytic prior. It was chosen for the 5-minute horizon on validation; the other horizons keep the 2-parameter recalibration.

| split | horizon | structural | full | full+recal | adaptive | Δ adaptive vs recal (millinats) |
|---|---|---|---|---|---|---|
| val | 5-minute (to close) | 0.5200 | 0.5190 | 0.5133 | 0.5128 | +0.43 [+0.02, +0.83] |
| val | 1-minute | 0.4211 | 0.4194 | 0.4190 | 0.4191 | -0.04 [-0.09, +0.01] |
| val | 30-second | 0.3225 | 0.3187 | 0.3181 | 0.3182 | -0.03 [-0.09, +0.02] |
| test | 5-minute (to close) | 0.4902 | 0.4900 | 0.4874 | 0.4865 | +0.90 [+0.59, +1.23] |
| test | 1-minute | 0.4253 | 0.4201 | 0.4202 | 0.4199 | +0.23 [+0.02, +0.52] |
| test | 30-second | 0.3257 | 0.3164 | 0.3163 | 0.3163 | +0.05 [-0.04, +0.17] |

### 5-minute model, continuously through the window (test)

| elapsed (s) | n | naive RW | structural | full | full+recal | AUC | accuracy |
|---|---|---|---|---|---|---|---|
| 0-0 | 44,352 | 0.6932 | 0.6914 | 0.6937 | 0.6937 | 0.528 | 0.520 |
| 1-59 | 261,695 | 0.6615 | 0.6531 | 0.6547 | 0.6547 | 0.652 | 0.604 |
| 60-119 | 266,112 | 0.6064 | 0.5836 | 0.5848 | 0.5848 | 0.756 | 0.686 |
| 120-179 | 266,112 | 0.5391 | 0.5024 | 0.5030 | 0.5025 | 0.832 | 0.752 |
| 180-239 | 266,112 | 0.4634 | 0.4067 | 0.4064 | 0.4042 | 0.897 | 0.815 |
| 240-299 | 266,112 | 0.3739 | 0.2743 | 0.2702 | 0.2594 | 0.959 | 0.898 |

At `e=0` the price is exactly at the reference, so the forecast is purely directional. That is the hardest case, and it is reported separately.

## 2. Pure direction from *now* (displacement removed)

This is P(S(t+h) > S(t)). It isolates genuine predictive power: no information comes from where the price sits relative to K.

| horizon | log loss | AUC | accuracy | top-10%-confidence accuracy | IC (Spearman) |
|---|---|---|---|---|---|
| 10-second | 0.6558 | 0.658 | 0.616 | 0.767 | 0.291 |
| 15-second | 0.6612 | 0.644 | 0.606 | 0.748 | 0.251 |
| 30-second | 0.6719 | 0.616 | 0.583 | 0.712 | 0.187 |
| 1-minute | 0.6815 | 0.585 | 0.560 | 0.663 | 0.132 |
| 5-minute (to close) | 0.6869 | 0.562 | 0.541 | 0.637 | 0.087 |

## 3. Magnitude and speed

| horizon | QLIKE naive → model | corr(log σ̂², log RV) naive → model | pinball (bps) naive → full | 50% cov | 90% cov |
|---|---|---|---|---|---|
| 10-second | 8.175 → **6.908** | 0.511 → **0.572** | 0.387 → **0.370** | 0.565 | 0.886 |
| 15-second | 6.223 → **4.937** | 0.538 → **0.592** | 0.497 → **0.477** | 0.552 | 0.888 |
| 30-second | 4.204 → **2.753** | 0.576 → **0.626** | 0.751 → **0.724** | 0.539 | 0.893 |
| 1-minute | 3.201 → **1.563** | 0.609 → **0.647** | 1.107 → **1.067** | 0.517 | 0.894 |
| 5-minute (to close) | 3.178 → **1.514** | 0.688 → **0.749** | 1.671 → **1.619** | 0.509 | 0.891 |

## 4. Levels: thresholds, touches, which comes first

### 10-second

| question | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| end ≥ K-20bp | – | 0.981 | 0.0162 | 0.0141 | **0.0140** | 0.998 |
| end ≥ K-10bp | – | 0.925 | 0.0544 | 0.0466 | **0.0464** | 0.994 |
| end ≥ K+10bp | – | 0.073 | 0.0535 | 0.0453 | **0.0451** | 0.994 |
| end ≥ K+20bp | – | 0.019 | 0.0162 | 0.0137 | **0.0136** | 0.998 |
| touch K+5bp | 1,145,295 | 0.030 | 0.1149 | 0.1242 | **0.0789** | 0.948 |
| touch K-5bp | 1,134,969 | 0.031 | 0.1221 | 0.1311 | **0.0830** | 0.945 |
| touch K+10bp | 1,276,013 | 0.014 | 0.0514 | 0.0535 | **0.0368** | 0.973 |
| touch K-10bp | 1,273,273 | 0.014 | 0.0527 | 0.0558 | **0.0376** | 0.973 |
| touch K+20bp | 1,346,632 | 0.004 | 0.0161 | 0.0157 | **0.0118** | 0.984 |
| touch K-20bp | 1,346,436 | 0.005 | 0.0159 | 0.0157 | **0.0118** | 0.986 |
| touch K+30bp | 1,362,091 | 0.002 | 0.0067 | 0.0062 | **0.0050** | 0.981 |
| touch K-30bp | 1,362,802 | 0.002 | 0.0065 | 0.0063 | **0.0049** | 0.985 |
| ±5bp: which first (3-class) | 1,370,465 | up-first 0.022 | 0.2100 | 0.2169 | **0.1544** | 0.671 (up vs down) |
| ±10bp: which first (3-class) | 1,370,489 | up-first 0.004 | 0.0457 | 0.0424 | **0.0311** | 0.678 (up vs down) |
| ±20bp: which first (3-class) | 1,370,495 | up-first 0.000 | 0.0081 | 0.0066 | **0.0049** | 0.758 (up vs down) |
| ±30bp: which first (3-class) | 1,370,495 | up-first 0.000 | 0.0025 | 0.0020 | **0.0016** | 0.764 (up vs down) |

### 15-second

| question | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| end ≥ K-20bp | – | 0.981 | 0.0212 | 0.0181 | **0.0180** | 0.996 |
| end ≥ K-10bp | – | 0.923 | 0.0706 | 0.0602 | **0.0601** | 0.991 |
| end ≥ K+10bp | – | 0.075 | 0.0692 | 0.0585 | **0.0584** | 0.991 |
| end ≥ K+20bp | – | 0.019 | 0.0211 | 0.0176 | **0.0176** | 0.996 |
| touch K+5bp | 1,145,295 | 0.043 | 0.1465 | 0.1439 | **0.1060** | 0.938 |
| touch K-5bp | 1,134,969 | 0.045 | 0.1543 | 0.1517 | **0.1113** | 0.935 |
| touch K+10bp | 1,276,013 | 0.020 | 0.0675 | 0.0642 | **0.0505** | 0.967 |
| touch K-10bp | 1,273,273 | 0.020 | 0.0691 | 0.0664 | **0.0515** | 0.967 |
| touch K+20bp | 1,346,632 | 0.006 | 0.0218 | 0.0196 | **0.0165** | 0.981 |
| touch K-20bp | 1,346,436 | 0.006 | 0.0213 | 0.0195 | **0.0163** | 0.982 |
| touch K+30bp | 1,362,091 | 0.003 | 0.0093 | 0.0081 | **0.0071** | 0.977 |
| touch K-30bp | 1,362,802 | 0.002 | 0.0087 | 0.0079 | **0.0067** | 0.981 |
| ±5bp: which first (3-class) | 1,370,462 | up-first 0.037 | 0.3069 | 0.2845 | **0.2318** | 0.656 (up vs down) |
| ±10bp: which first (3-class) | 1,370,489 | up-first 0.007 | 0.0768 | 0.0663 | **0.0539** | 0.665 (up vs down) |
| ±20bp: which first (3-class) | 1,370,495 | up-first 0.001 | 0.0140 | 0.0112 | **0.0087** | 0.734 (up vs down) |
| ±30bp: which first (3-class) | 1,370,495 | up-first 0.000 | 0.0045 | 0.0037 | **0.0029** | 0.759 (up vs down) |

### 30-second

| question | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| end ≥ K-20bp | – | 0.979 | 0.0331 | 0.0279 | **0.0278** | 0.991 |
| end ≥ K-10bp | – | 0.917 | 0.1085 | 0.0920 | **0.0919** | 0.979 |
| end ≥ K+10bp | – | 0.081 | 0.1078 | 0.0901 | **0.0899** | 0.979 |
| end ≥ K+20bp | – | 0.021 | 0.0343 | 0.0278 | **0.0277** | 0.991 |
| touch K+5bp | 1,145,295 | 0.076 | 0.2190 | 0.2049 | **0.1691** | 0.916 |
| touch K-5bp | 1,134,969 | 0.079 | 0.2299 | 0.2142 | **0.1761** | 0.913 |
| touch K+10bp | 1,276,013 | 0.036 | 0.1106 | 0.0983 | **0.0851** | 0.952 |
| touch K-10bp | 1,273,273 | 0.037 | 0.1120 | 0.1011 | **0.0866** | 0.952 |
| touch K+20bp | 1,346,632 | 0.011 | 0.0383 | 0.0325 | **0.0291** | 0.973 |
| touch K-20bp | 1,346,436 | 0.011 | 0.0365 | 0.0315 | **0.0281** | 0.977 |
| touch K+30bp | 1,362,091 | 0.005 | 0.0166 | 0.0140 | **0.0127** | 0.972 |
| touch K-30bp | 1,362,802 | 0.004 | 0.0155 | 0.0132 | **0.0118** | 0.980 |
| ±5bp: which first (3-class) | 1,370,455 | up-first 0.079 | 0.5274 | 0.4840 | **0.4143** | 0.629 (up vs down) |
| ±10bp: which first (3-class) | 1,370,487 | up-first 0.018 | 0.1758 | 0.1457 | **0.1273** | 0.638 (up vs down) |
| ±20bp: which first (3-class) | 1,370,494 | up-first 0.003 | 0.0352 | 0.0279 | **0.0232** | 0.720 (up vs down) |
| ±30bp: which first (3-class) | 1,370,495 | up-first 0.001 | 0.0122 | 0.0099 | **0.0077** | 0.769 (up vs down) |

### 1-minute

| question | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| end ≥ K-20bp | – | 0.975 | 0.0552 | 0.0450 | **0.0449** | 0.979 |
| end ≥ K-10bp | – | 0.905 | 0.1675 | 0.1405 | **0.1404** | 0.955 |
| end ≥ K+10bp | – | 0.093 | 0.1670 | 0.1381 | **0.1380** | 0.955 |
| end ≥ K+20bp | – | 0.025 | 0.0571 | 0.0453 | **0.0453** | 0.977 |
| touch K+5bp | 1,145,295 | 0.129 | 0.3247 | 0.2929 | **0.2587** | 0.886 |
| touch K-5bp | 1,134,969 | 0.134 | 0.3348 | 0.3016 | **0.2656** | 0.884 |
| touch K+10bp | 1,276,013 | 0.064 | 0.1838 | 0.1559 | **0.1424** | 0.927 |
| touch K-10bp | 1,273,273 | 0.065 | 0.1843 | 0.1588 | **0.1441** | 0.928 |
| touch K+20bp | 1,346,632 | 0.020 | 0.0700 | 0.0573 | **0.0529** | 0.960 |
| touch K-20bp | 1,346,436 | 0.021 | 0.0677 | 0.0555 | **0.0513** | 0.964 |
| touch K+30bp | 1,362,091 | 0.008 | 0.0321 | 0.0260 | **0.0240** | 0.967 |
| touch K-30bp | 1,362,802 | 0.008 | 0.0295 | 0.0242 | **0.0222** | 0.972 |
| ±5bp: which first (3-class) | 1,370,442 | up-first 0.149 | 0.7838 | 0.7301 | **0.6339** | 0.604 (up vs down) |
| ±10bp: which first (3-class) | 1,370,487 | up-first 0.046 | 0.3594 | 0.2944 | **0.2662** | 0.609 (up vs down) |
| ±20bp: which first (3-class) | 1,370,494 | up-first 0.008 | 0.0907 | 0.0717 | **0.0619** | 0.680 (up vs down) |
| ±30bp: which first (3-class) | 1,370,495 | up-first 0.002 | 0.0335 | 0.0268 | **0.0218** | 0.739 (up vs down) |

### 5-minute (to close)

| question | n | base rate | naive LL | structural LL | full LL | full AUC |
|---|---|---|---|---|---|---|
| end ≥ K-20bp | – | 0.964 | 0.1052 | 0.0838 | **0.0837** | 0.944 |
| end ≥ K-10bp | – | 0.875 | 0.2561 | 0.2198 | **0.2198** | 0.910 |
| end ≥ K+10bp | – | 0.124 | 0.2610 | 0.2189 | **0.2190** | 0.909 |
| end ≥ K+20bp | – | 0.038 | 0.1078 | 0.0851 | **0.0850** | 0.943 |
| touch K+5bp | 1,145,295 | 0.232 | 0.4544 | 0.4138 | **0.3739** | 0.863 |
| touch K-5bp | 1,134,969 | 0.237 | 0.4551 | 0.4177 | **0.3767** | 0.864 |
| touch K+10bp | 1,276,013 | 0.129 | 0.3225 | 0.2723 | **0.2548** | 0.888 |
| touch K-10bp | 1,273,273 | 0.129 | 0.3125 | 0.2720 | **0.2519** | 0.892 |
| touch K+20bp | 1,346,632 | 0.043 | 0.1509 | 0.1199 | **0.1125** | 0.925 |
| touch K-20bp | 1,346,436 | 0.044 | 0.1474 | 0.1172 | **0.1097** | 0.930 |
| touch K+30bp | 1,362,091 | 0.018 | 0.0754 | 0.0588 | **0.0549** | 0.945 |
| touch K-30bp | 1,362,802 | 0.018 | 0.0725 | 0.0577 | **0.0531** | 0.948 |
| ±5bp: which first (3-class) | 1,370,444 | up-first 0.240 | 0.9124 | 0.8867 | **0.7510** | 0.572 (up vs down) |
| ±10bp: which first (3-class) | 1,370,490 | up-first 0.110 | 0.6178 | 0.5312 | **0.4791** | 0.566 (up vs down) |
| ±20bp: which first (3-class) | 1,370,494 | up-first 0.030 | 0.2542 | 0.2012 | **0.1812** | 0.597 (up vs down) |
| ±30bp: which first (3-class) | 1,370,495 | up-first 0.011 | 0.1177 | 0.0933 | **0.0801** | 0.653 (up vs down) |

## 5. Consistency

### Month by month (main test, 5-minute model, Δ log loss in millinats)

| month | full vs naive RW | full vs structural |
|---|---|---|
| 2026-06 | +31.8 | -0.1 |
| 2026-07 | +55.7 | +0.2 |
| 2026-08 | +37.2 | +2.2 |
| 2026-09 | +43.9 | -1.0 |
| 2026-10 | +50.1 | -0.5 |
| 2026-11 | +23.1 | -1.5 |

### Walk-forward (full retrain on an expanding window for each fold)

| fold | test period | horizon | naive RW | full | full+recal | Δ full vs naive | dir. AUC |
|---|---|---|---|---|---|---|---|
| A | 2025-05-01 → 2025-09-01 | 30-second | 0.3461 | 0.3085 | 0.3083 | +37.6 [+34.9, +40.9] | 0.620 |
| A | 2025-05-01 → 2025-09-01 | 1-minute | 0.4475 | 0.4148 | 0.4147 | +32.7 [+30.4, +34.9] | 0.586 |
| A | 2025-05-01 → 2025-09-01 | 5-minute (to close) | 0.4714 | 0.4505 | 0.4507 | +20.9 [+19.0, +23.0] | 0.568 |
| B | 2025-11-01 → 2026-03-01 | 30-second | 0.3490 | 0.3233 | 0.3231 | +25.7 [+22.2, +30.1] | 0.581 |
| B | 2025-11-01 → 2026-03-01 | 1-minute | 0.4449 | 0.4243 | 0.4239 | +20.6 [+17.9, +23.9] | 0.557 |
| B | 2025-11-01 → 2026-03-01 | 5-minute (to close) | 0.4799 | 0.4643 | 0.4641 | +15.6 [+12.8, +18.4] | 0.549 |
| val | 2026-03-01 → 2026-06-01 | 10-second | 0.2251 | 0.1928 | 0.1925 | +32.3 [+28.9, +35.4] | 0.650 |
| val | 2026-03-01 → 2026-06-01 | 15-second | 0.2635 | 0.2334 | 0.2330 | +30.1 [+26.8, +33.5] | 0.635 |
| val | 2026-03-01 → 2026-06-01 | 30-second | 0.3453 | 0.3187 | 0.3181 | +26.6 [+23.7, +29.8] | 0.603 |
| val | 2026-03-01 → 2026-06-01 | 1-minute | 0.4418 | 0.4194 | 0.4191 | +22.4 [+20.3, +24.8] | 0.570 |
| val | 2026-03-01 → 2026-06-01 | 5-minute (to close) | 0.5698 | 0.5190 | 0.5133 | +50.8 [+42.6, +58.7] | 0.553 |
| main | 2026-06-01 → 2026-11-03 | 10-second | 0.2332 | 0.1898 | 0.1898 | +43.4 [+39.5, +47.7] | 0.658 |
| main | 2026-06-01 → 2026-11-03 | 15-second | 0.2741 | 0.2307 | 0.2307 | +43.4 [+39.5, +47.7] | 0.644 |
| main | 2026-06-01 → 2026-11-03 | 30-second | 0.3579 | 0.3164 | 0.3163 | +41.5 [+37.8, +45.7] | 0.616 |
| main | 2026-06-01 → 2026-11-03 | 1-minute | 0.4562 | 0.4201 | 0.4202 | +36.1 [+33.3, +39.3] | 0.585 |
| main | 2026-06-01 → 2026-11-03 | 5-minute (to close) | 0.5337 | 0.4900 | 0.4875 | +43.7 [+38.1, +49.8] | 0.562 |
| main (v1 recipe) | 2026-06-01 → 2026-11-03 | 30-second | 0.3579 | 0.3161 | 0.3160 | +41.8 [+38.0, +46.0] | 0.617 |
| main (v1 recipe) | 2026-06-01 → 2026-11-03 | 1-minute | 0.4562 | 0.4199 | 0.4199 | +36.3 [+33.4, +39.5] | 0.585 |
| main (v1 recipe) | 2026-06-01 → 2026-11-03 | 5-minute (to close) | 0.5337 | 0.4896 | 0.4867 | +44.2 [+38.9, +50.2] | 0.564 |

(`val` was used for early stopping, so it is slightly optimistic. It is shown for completeness.)

## 6. Robustness across market regimes

Regime variables are causal (only previous days), and their thresholds are fixed on the training period. Each cell is the 5-minute log-loss improvement over the naive random walk in millinats, with a 95% day-block CI, plus AUC. The edge has to hold in **every** slice, not just on average.

### main test (Jun–Nov 2026: bear low and rebound)

| regime family | slice | windows | Δ 5-min [95% CI] | 5-min AUC | Δ 1-min | Δ 30s | 30s direction AUC |
|---|---|---|---|---|---|---|---|
| all | all | 44,352 | +43.7 [+38.2, +49.4] | 0.838 | +36.1 | +41.5 | 0.616 |
| volatility regime (7-day) | calm | 29,664 | +49.3 [+41.4, +56.3] | 0.837 | +41.8 | +48.0 | 0.625 |
| volatility regime (7-day) | normal | 8,640 | +37.2 [+23.8, +49.5] | 0.837 | +28.1 | +32.8 | 0.604 |
| volatility regime (7-day) | turbulent | 6,048 | +25.6 [+18.2, +33.6] | 0.843 | +20.1 | +22.1 | 0.587 |
| trend regime (7-day) | bear | 17,280 | +39.0 [+31.2, +47.8] | 0.840 | +34.8 | +39.4 | 0.607 |
| trend regime (7-day) | sideways | 14,112 | +54.7 [+45.1, +65.8] | 0.833 | +40.8 | +47.0 | 0.627 |
| trend regime (7-day) | bull | 12,960 | +38.0 [+30.1, +47.5] | 0.840 | +32.9 | +38.5 | 0.613 |
| drawdown from 30-day high | deep (< -3 daily sd) | 16,704 | +35.6 [+29.9, +43.5] | 0.841 | +32.8 | +37.0 | 0.607 |
| drawdown from 30-day high | shallow | 27,648 | +48.6 [+41.1, +55.8] | 0.836 | +38.2 | +44.2 | 0.621 |
| vol expansion (7d vs 30d) | expanding (> +0.3) | 5,472 | +21.5 [+15.0, +27.6] | 0.848 | +21.3 | +23.2 | 0.583 |
| vol expansion (7d vs 30d) | stable/contracting | 38,880 | +46.8 [+40.2, +54.5] | 0.836 | +38.2 | +44.1 | 0.620 |
| intraday activity (1-hour vol) | quiet hour | 21,592 | +71.6 [+64.2, +78.8] | 0.824 | +51.5 | +62.7 | 0.647 |
| intraday activity (1-hour vol) | normal hour | 16,091 | +24.8 [+21.6, +28.2] | 0.849 | +26.5 | +27.5 | 0.601 |
| intraday activity (1-hour vol) | hot hour | 9,081 | +9.0 [+6.3, +11.8] | 0.851 | +15.8 | +14.8 | 0.560 |
| calendar | weekday | 31,680 | +30.6 [+27.2, +34.7] | 0.844 | +29.9 | +31.6 | 0.606 |
| calendar | weekend | 12,672 | +76.4 [+63.2, +89.6] | 0.822 | +51.8 | +66.4 | 0.640 |

### walk-forward fold A (May–Aug 2025: bull run)

| regime family | slice | windows | Δ 5-min [95% CI] | 5-min AUC | Δ 1-min | Δ 30s | 30s direction AUC |
|---|---|---|---|---|---|---|---|
| all | all | 35,136 | +20.9 [+19.0, +23.0] | 0.863 | +32.7 | +37.6 | 0.620 |
| volatility regime (7-day) | calm | 34,560 | +21.0 [+18.9, +23.0] | 0.863 | +32.8 | +37.8 | 0.620 |
| volatility regime (7-day) | normal | 576 | +17.2 [+13.7, +20.7] | 0.855 | +25.4 | +29.5 | 0.620 |
| trend regime (7-day) | bear | 11,232 | +20.7 [+17.5, +24.1] | 0.863 | +30.9 | +34.2 | 0.619 |
| trend regime (7-day) | sideways | 13,536 | +23.9 [+20.1, +27.6] | 0.863 | +35.7 | +42.0 | 0.628 |
| trend regime (7-day) | bull | 10,368 | +17.2 [+14.4, +20.4] | 0.861 | +30.7 | +35.7 | 0.610 |
| drawdown from 30-day high | deep (< -3 daily sd) | 8,064 | +21.8 [+18.8, +25.0] | 0.864 | +35.4 | +39.7 | 0.626 |
| drawdown from 30-day high | shallow | 27,072 | +20.6 [+18.0, +23.2] | 0.862 | +31.9 | +37.0 | 0.618 |
| vol expansion (7d vs 30d) | expanding (> +0.3) | 3,168 | +16.8 [+12.7, +19.6] | 0.865 | +27.4 | +31.1 | 0.612 |
| vol expansion (7d vs 30d) | stable/contracting | 31,968 | +21.3 [+19.0, +23.4] | 0.862 | +33.2 | +38.3 | 0.621 |
| intraday activity (1-hour vol) | quiet hour | 21,912 | +26.0 [+23.7, +28.9] | 0.865 | +41.0 | +48.9 | 0.643 |
| intraday activity (1-hour vol) | normal hour | 11,288 | +15.4 [+12.7, +18.2] | 0.857 | +22.6 | +23.3 | 0.591 |
| intraday activity (1-hour vol) | hot hour | 3,521 | +5.2 [+1.6, +8.7] | 0.862 | +10.8 | +10.5 | 0.558 |
| calendar | weekday | 25,056 | +18.6 [+16.3, +20.5] | 0.863 | +28.5 | +30.9 | 0.612 |
| calendar | weekend | 10,080 | +26.6 [+22.8, +30.3] | 0.862 | +43.1 | +54.3 | 0.641 |

### walk-forward fold B (Nov 2025–Feb 2026: crash −43%)

| regime family | slice | windows | Δ 5-min [95% CI] | 5-min AUC | Δ 1-min | Δ 30s | 30s direction AUC |
|---|---|---|---|---|---|---|---|
| all | all | 34,272 | +15.6 [+12.8, +18.4] | 0.853 | +20.6 | +25.7 | 0.581 |
| volatility regime (7-day) | calm | 9,216 | +20.9 [+15.5, +25.7] | 0.856 | +32.1 | +40.6 | 0.611 |
| volatility regime (7-day) | normal | 14,688 | +14.7 [+11.2, +18.8] | 0.856 | +20.7 | +25.8 | 0.583 |
| volatility regime (7-day) | turbulent | 10,368 | +12.3 [+7.0, +18.4] | 0.846 | +10.2 | +12.1 | 0.552 |
| trend regime (7-day) | bear | 18,144 | +10.9 [+8.1, +14.4] | 0.854 | +15.3 | +18.7 | 0.568 |
| trend regime (7-day) | sideways | 10,944 | +19.9 [+14.9, +24.9] | 0.853 | +25.0 | +32.3 | 0.594 |
| trend regime (7-day) | bull | 5,184 | +22.9 [+16.1, +29.4] | 0.850 | +30.0 | +36.0 | 0.603 |
| drawdown from 30-day high | deep (< -3 daily sd) | 24,192 | +13.0 [+10.0, +16.9] | 0.852 | +15.3 | +18.3 | 0.569 |
| drawdown from 30-day high | shallow | 10,080 | +21.9 [+17.6, +26.5] | 0.856 | +33.4 | +43.4 | 0.612 |
| vol expansion (7d vs 30d) | expanding (> +0.3) | 7,200 | +8.7 [+4.8, +12.6] | 0.852 | +10.1 | +12.6 | 0.550 |
| vol expansion (7d vs 30d) | stable/contracting | 27,072 | +17.4 [+14.1, +20.4] | 0.853 | +23.4 | +29.2 | 0.589 |
| intraday activity (1-hour vol) | quiet hour | 9,406 | +32.2 [+28.4, +36.8] | 0.851 | +44.4 | +58.3 | 0.634 |
| intraday activity (1-hour vol) | normal hour | 11,769 | +14.6 [+11.0, +18.6] | 0.850 | +17.9 | +21.2 | 0.585 |
| intraday activity (1-hour vol) | hot hour | 14,805 | +6.0 [+3.7, +8.2] | 0.857 | +7.8 | +8.6 | 0.544 |
| calendar | weekday | 24,480 | +10.8 [+8.4, +13.0] | 0.855 | +15.3 | +18.4 | 0.572 |
| calendar | weekend | 9,792 | +27.7 [+21.4, +34.0] | 0.848 | +33.9 | +43.8 | 0.607 |

### How regime handling was chosen (validation period only)

| horizon | configuration | above-ref LL | Δ vs base (millinats) | vol QLIKE | drift IC |
|---|---|---|---|---|---|
| 30-second | base | 0.32280 | +0.00 | 2.1744 | 0.1689 |
| 30-second | base+decay180 | 0.32248 | -0.32 | 2.1732 | 0.1685 |
| 30-second | base+decay365 | 0.32258 | -0.22 | 2.1744 | 0.1690 |
| 30-second | +regime | 0.32269 | -0.11 | 2.1740 | 0.1690 |
| 30-second | +regime+decay180 | 0.32248 | -0.32 | 2.1703 | 0.1685 |
| 30-second | +regime+decay365 | 0.32258 | -0.23 | 2.1707 | 0.1691 |
| 30-second | +regime (vol-engine only) | 0.32273 | -0.08 | 2.1741 | 0.1691 |
| 30-second | +regime+decay180 (vol-engine only) | 0.32253 | -0.27 | 2.1704 | 0.1684 |
| 5-minute (to close) | base | 0.52310 | +0.00 | 1.2091 | 0.0778 |
| 5-minute (to close) | base+decay180 | 0.52298 | -0.12 | 1.2017 | 0.0789 |
| 5-minute (to close) | base+decay365 | 0.52297 | -0.12 | 1.2032 | 0.0774 |
| 5-minute (to close) | +regime | 0.52340 | +0.30 | 1.2104 | 0.0763 |
| 5-minute (to close) | +regime+decay180 | 0.52272 | -0.38 | 1.2020 | 0.0752 |
| 5-minute (to close) | +regime+decay365 | 0.52272 | -0.38 | 1.2095 | 0.0770 |
| 5-minute (to close) | +regime (vol-engine only) | 0.52331 | +0.22 | 1.2107 | 0.0774 |
| 5-minute (to close) | +regime+decay180 (vol-engine only) | 0.52254 | -0.56 | 1.2028 | 0.0770 |

When regime variables are offered to the directional models they are used as *directional* signals: they take 13% of the 5-minute drift gain and make validation worse. Two years contain too few distinct regimes to learn regime-dependent drift. So regime state is allowed only to scale volatility and tails, the same rule as for calendar features, and recent data is up-weighted with a 180-day half-life. That configuration is the best on validation for both horizons and in every validation month.

## 7. What drives the predictions (ablations on the validation period)

### 30-second

| feature set | drift IC | direction AUC | above-ref LL (structural) | Δ LL vs all (millinats) | vol QLIKE |
|---|---|---|---|---|---|
| all | 0.1689 | 0.6021 | 0.32280 | +0.00 | 2.1744 |
| no_futures | 0.1128 | 0.5639 | 0.32580 | +3.00 | 2.1801 |
| no_flow | 0.1673 | 0.6016 | 0.32298 | +0.17 | 2.1728 |
| no_window_state | 0.1684 | 0.6019 | 0.32273 | -0.07 | 2.1749 |
| no_round_levels | 0.1682 | 0.6018 | 0.32286 | +0.05 | 2.1738 |
| no_momentum | 0.1637 | 0.5991 | 0.32356 | +0.76 | 2.1783 |
| spot_price_only | 0.1064 | 0.5599 | 0.32621 | +3.41 | 2.1786 |

A linear (ridge) drift model on the same features reaches IC 0.1582 (AUC 0.5938), against 0.1689 for LightGBM.

Top drift features (gain share): `basis_dev_300` 0.27, `basis_dev_60` 0.20, `basis_dev_3600` 0.05, `zfret_5` 0.04, `zfret_1` 0.03, `zfret_10` 0.03, `lew_120` 0.02, `zfret_2` 0.02, `zfret_3` 0.02, `fofi_5` 0.02

### 1-minute

| feature set | drift IC | direction AUC | above-ref LL (structural) | Δ LL vs all (millinats) | vol QLIKE |
|---|---|---|---|---|---|
| all | 0.1202 | 0.5703 | 0.40796 | +0.00 | 1.1312 |
| no_futures | 0.0764 | 0.5419 | 0.41043 | +2.47 | 1.1363 |
| no_flow | 0.1181 | 0.5694 | 0.40806 | +0.10 | 1.1309 |
| no_window_state | 0.1201 | 0.5703 | 0.40781 | -0.15 | 1.1343 |
| no_round_levels | 0.1202 | 0.5703 | 0.40790 | -0.06 | 1.1313 |
| no_momentum | 0.1176 | 0.5689 | 0.40836 | +0.40 | 1.1364 |
| spot_price_only | 0.0725 | 0.5391 | 0.41062 | +2.66 | 1.1357 |

A linear (ridge) drift model on the same features reaches IC 0.1122 (AUC 0.5648), against 0.1202 for LightGBM.

Top drift features (gain share): `basis_dev_300` 0.22, `basis_dev_60` 0.14, `basis_dev_3600` 0.06, `zfret_5` 0.03, `lew_120` 0.02, `zfret_1` 0.02, `zfret_10` 0.02, `zfret_2` 0.01, `fofi_5` 0.01, `zfret_3` 0.01

### Architecture experiment: temporal CNN on raw 1-second sequences

- **30-second**: the CNN alone has IC 0.1619; LightGBM drift alone 0.1666; the blend (weight on the CNN 0.3, chosen on held-out days) 0.1673. Correlation between the two forecasts: 0.94.

## 8. Independent audit

`scripts/12_audit.py` recomputes the 5-minute labels and the naive baseline directly from the raw 1-second files,
sharing no code with the feature pipeline. On the test period:
* **0 mismatches** in K or in the window close over 1,370,489 decision rows (44,352 windows);
* ties (`close == K`) occur in 0.44% of windows;
* the up-rate is 49.9%;
* the naive log loss recomputed independently is 0.5346, against 0.5337 in the pipeline (rounding of the
  volatility proxy).

## 9. Limitations and honest caveats

* **Reference source.** The model is trained on Binance BTCUSDT spot. If your reference and settlement price
  comes from another source (Chainlink BTC/USD streams, Coinbase, an index), the lead-lag structure and the tie
  behaviour change. Rebuild the labels on that series; the pipeline is source-agnostic.
* **Latency.** The lead-lag edge lives at the 1–3 second scale. The live engine needs both feeds with low
  latency, and stale perp data silently removes most of the directional skill. Ablations show that removing
  the perp features costs about a third of the 30s drift IC.
* **Window-open direction is close to efficient.** At `e = 0` the 5-minute AUC is about 0.53. The boosted head is
  slightly worse than the analytic prior there; validation and test agree. The adaptive ensemble therefore
  falls back to the prior at the open (test log loss 0.6917, against 0.6937 for the head alone). The value of the
  5-minute model is in continuous re-pricing through the window, not in calling the direction at the open. For
  that, the 10s–60s models are much stronger.
* **Calibration drift.** In 2026 the raw 5-minute head is slightly over-confident at the extremes. The causal
  14-day trailing recalibration removes this (ECE 0.014 → 0.003 on test). The live engine refits it daily from
  its own resolved predictions.
* **Explicit regime features add little.** Multi-day regime state in the volatility engine plus 180-day recency
  weighting (the v2 recipe) is statistically indistinguishable from v1 on both validation and test (≤ 0.8 millinats,
  inside the CIs). The robustness comes from volatility-standardised inputs, causal recalibration and the adaptive
  ensemble, not from regime labels. v2 is kept as the production recipe because it was the validation choice and
  adapts faster to structural change; v1 results are reported alongside.
* **No transaction costs or market prices.** Log-loss gains are statistical skill. Turning them into profit
  against a real order book or prediction market depends on its prices, fees and latency, none of which are
  modelled here.
* **Regime risk.** Three fully separate retrains were tested on a bull run (May–Aug 2025), a 43% crash (Nov 2025 – Feb
  2026) and a bear low and rebound (Jun–Nov 2026). They improve on the naive baseline in every month and every
  regime slice. The edge is smallest in the crash fold: the 5-minute gain is +15.6 millinats there against +44 in
  2026, and the 30s direction AUC is 0.58 against 0.62. It is also smallest in the busiest hours, where spot catches
  up with the perpetual fastest. A structural change in market microstructure (for example a venue migration of
  price discovery) would require retraining with `scripts/11_train_production.sh`; the live `regime_alert` is
  designed to tell you when.
* **Architecture.** A temporal CNN reading the raw last 60 seconds learns a forecast that is 0.94 correlated with
  the gradient-boosted drift and adds no incremental IC (§7). The edge is captured by the engineered features. More
  model capacity is unlikely to help; more *information* (order-book data, other venues) is where further gains
  would come from.
