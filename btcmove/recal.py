"""Causal trailing recalibration (adapts to regime drift without look-ahead).

For each UTC day d, a 2-parameter logistic map p' = sigmoid(a * logit(p) + b) is fitted on the rows of
days [d - lookback, d) whose outcomes are already known (all labels resolve within 6 minutes; rows of the
final hour before d are excluded for safety) and applied to day d.  Optionally fitted per elapsed-time
bucket.  The same object is used in the live engine (refit once per day from logged predictions).
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize

from .structural import logit, sigmoid


def _fit_ab(z, y, w=None, l2=1.0):
    w = np.ones_like(z) if w is None else w

    def f(p):
        a, b = p
        s = a * z + b
        ll = np.sum(w * (np.logaddexp(0, s) - y * s)) / w.sum()
        return ll + l2 * ((a - 1) ** 2 + b ** 2) / len(z)

    def g(p):
        a, b = p
        s = a * z + b
        r = w * (sigmoid(s) - y) / w.sum()
        return np.array([np.sum(r * z) + 2 * l2 * (a - 1) / len(z), np.sum(r) + 2 * l2 * b / len(z)])

    o = minimize(f, x0=np.array([1.0, 0.0]), jac=g, method="L-BFGS-B", bounds=[(0.5, 2.0), (-1, 1)])
    return o.x


def trailing_recalibrate(ts, p, y, lookback_days=14, gap_s=3600, min_rows=20000, groups=None):
    """Return recalibrated probabilities for every row (rows without enough history are left unchanged)."""
    ts = np.asarray(ts); p = np.asarray(p, float); y = np.asarray(y, float)
    z = logit(p)
    day = ts // 86400
    out = p.copy()
    groups = np.zeros(len(p), int) if groups is None else np.asarray(groups)
    for d in np.unique(day):
        cur = day == d
        hist = (ts >= d * 86400 - lookback_days * 86400) & (ts < d * 86400 - gap_s)
        for g in np.unique(groups[cur]):
            hm = hist & (groups == g)
            cm = cur & (groups == g)
            if hm.sum() < min_rows:
                continue
            a, b = _fit_ab(z[hm], y[hm])
            out[cm] = sigmoid(a * z[cm] + b)
    return out


E_EDGES = (1, 60, 120, 180, 240)


class Recalibrator:
    """Per-(horizon, elapsed-bucket) logistic recalibration of P(above reference), refitted daily.

    params[H][g] = (a, b).  `fit` uses only rows whose outcome is known and that are older than
    `gap_s`; `apply` maps raw probabilities.  Identity until enough history is available.
    """

    def __init__(self, params: dict | None = None, lookback_days: int = 14, min_rows: int = 5000):
        self.params = params or {}
        self.lookback_days = lookback_days
        self.min_rows = min_rows

    @staticmethod
    def group(e):
        return np.digitize(np.asarray(e), E_EDGES)

    def fit(self, H, ts, e, p, y, now_ts, gap_s=3600):
        ts = np.asarray(ts); m = (ts >= now_ts - self.lookback_days * 86400) & (ts < now_ts - gap_s)
        g = self.group(e)
        z = logit(np.asarray(p, float))
        y = np.asarray(y, float)
        out = dict(self.params.get(H, {}))
        for k in np.unique(g[m]):
            mk = m & (g == k)
            if mk.sum() >= self.min_rows:
                out[int(k)] = tuple(float(v) for v in _fit_ab(z[mk], y[mk]))
        self.params[H] = out

    def apply(self, H, e, p):
        if H not in self.params or not self.params[H]:
            return np.asarray(p, float)
        g = self.group(e)
        z = logit(np.asarray(p, float))
        out = np.asarray(p, float).copy()
        for k, (a, b) in self.params[H].items():
            m = g == int(k)
            out[m] = sigmoid(a * z[m] + b)
        return out

    def to_json(self):
        return {"lookback_days": self.lookback_days, "params": {H: {str(k): v for k, v in d.items()} for H, d in self.params.items()}}

    @classmethod
    def from_json(cls, d):
        return cls({H: {int(k): tuple(v) for k, v in g.items()} for H, g in d["params"].items()}, d.get("lookback_days", 14))
