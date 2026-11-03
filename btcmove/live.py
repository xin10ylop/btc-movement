"""Real-time inference: a rolling 1-second buffer that reuses *exactly* the batch feature code.

Serving uses the same `features.compute` used for training (no train/serve skew).  At each second
boundary the bars of every completed second are known; the decision row is the start of the new second.

    pred = LivePredictor.from_artifacts("artifacts/models")
    pred.warmup(spot_bars, fut_bars)           # >= 2 days of history recommended
    out = pred.on_second(spot_bar, fut_bar)    # call once per completed second -> dict of predictions

`replay()` drives the predictor from the historical archive and is used by tests to prove that
streaming predictions equal batch predictions.

`run_binance()` is a minimal connector for Binance public websockets (spot kline_1s + USDT-M perpetual
aggTrade).  It needs network access to Binance (api.binance.com may be geo-restricted in some regions).
"""
from __future__ import annotations

import json
import time
from collections import deque
from pathlib import Path

import numpy as np
import pandas as pd

from . import features as fe
from .engine import Engine

BUF = 2 * 86400 + 3600
SPOT_FIELDS = ("o", "h", "l", "c", "v", "qv", "tbv", "n")
FUT_FIELDS = ("fc", "fv", "ftbv", "fn")


class RollingBuffer:
    def __init__(self, size: int = BUF):
        self.size = size
        self.a = {k: np.full(size + 1, np.nan if k in ("o", "h", "l", "c", "fc") else 0.0) for k in SPOT_FIELDS + FUT_FIELDS}
        self.n = 0           # number of filled bars
        self.ts_last = None  # ts of the last filled bar

    def push(self, ts: int, spot: dict, fut: dict | None):
        if self.ts_last is not None and ts != self.ts_last + 1:
            # fill gaps with flat bars (causal forward fill)
            for g in range(self.ts_last + 1, ts):
                self._append(g, None, None)
        self._append(ts, spot, fut)

    def _append(self, ts, spot, fut):
        if self.n == self.size:
            for k in self.a:
                self.a[k][:-1] = np.roll(self.a[k][:-1], -1)  # O(size); fine at 1 Hz
            j = self.size - 1
        else:
            j = self.n
            self.n += 1
        prevc = self.a["c"][j - 1] if j > 0 else np.nan
        prevf = self.a["fc"][j - 1] if j > 0 else np.nan
        if spot is None:
            for k in ("o", "h", "l", "c"):
                self.a[k][j] = prevc
            for k in ("v", "qv", "tbv", "n"):
                self.a[k][j] = 0.0
        else:
            for k in SPOT_FIELDS:
                self.a[k][j] = spot[k]
        if fut is None or not np.isfinite(fut.get("fc", np.nan)):
            self.a["fc"][j] = prevf
            for k in ("fv", "ftbv", "fn"):
                self.a[k][j] = 0.0
        else:
            for k in FUT_FIELDS:
                self.a[k][j] = fut[k]
        self.ts_last = ts

    def series(self, k_open: float | None) -> tuple[dict, int]:
        """Series dict of length n+1 (last element = the not-yet-complete current second).
        If the current second opens a new 5-minute window, its open is set to K."""
        n = self.n
        s = {k: v[: n + 1].copy() for k, v in self.a.items()}
        for k in ("o", "h", "l", "c", "fc"):
            s[k][n] = s[k][n - 1]
        for k in ("v", "qv", "tbv", "n", "fv", "ftbv", "fn"):
            s[k][n] = 0.0
        if k_open is not None:
            s["o"][n] = k_open
        s["start"] = self.ts_last - n + 1
        return s, n


class LivePredictor:
    def __init__(self, engine: Engine, seasonal: dict | None, quantiles: bool = True):
        self.engine = engine
        self.seasonal = seasonal
        self.buf = RollingBuffer()
        self.quantiles = quantiles

    @classmethod
    def from_artifacts(cls, mdir="artifacts/models", seasonal_path="data/seasonal.npz", **kw):
        eng = Engine.load(mdir)
        seas = None
        if Path(seasonal_path).exists():
            z = np.load(seasonal_path)
            seas = {k: (int(z[k]) if k == "ts0" else z[k]) for k in z.files}
        return cls(eng, seas, **kw)

    def _seasonal_for(self, ts):
        if self.seasonal is None:
            return None
        s = self.seasonal
        nd = s["tod"].shape[0]
        day = (ts - s["ts0"]) // 86400
        if day < nd:
            return s
        # beyond the stored history: reuse the latest profile (28-day average, changes slowly)
        extra = int(day - nd + 1)
        return {"ts0": s["ts0"], "tod": np.vstack([s["tod"], np.repeat(s["tod"][-1:], extra, 0)]),
                "sec": np.vstack([s["sec"], np.repeat(s["sec"][-1:], extra, 0)]),
                "sec_cum": np.vstack([s["sec_cum"], np.repeat(s["sec_cum"][-1:], extra, 0)])}

    def warmup(self, ts: np.ndarray, spot: dict, fut: dict | None = None):
        for i, t in enumerate(ts):
            self.buf.push(int(t), {k: spot[k][i] for k in SPOT_FIELDS},
                          None if fut is None else {k: fut[k][i] for k in FUT_FIELDS})

    def features_now(self, k_open: float | None = None) -> pd.DataFrame:
        """Feature row for the decision at the start of second ts_last+1."""
        ts_now = self.buf.ts_last + 1
        e = ts_now % fe.WIN
        if e == 0 and k_open is None:
            k_open = float(self.buf.a["c"][self.buf.n - 1])  # best available until the first trade prints
        ser, idx = self.buf.series(k_open if e == 0 else None)
        F = fe.compute(ser, np.array([idx]), seasonal=self._seasonal_for(ts_now), with_targets=False)
        return pd.DataFrame({k: np.asarray(v) for k, v in F.items()})

    def push(self, ts: int, spot: dict, fut: dict | None):
        self.buf.push(ts, spot, fut)

    def predict(self, k_open: float | None = None) -> dict:
        row = self.features_now(k_open)
        return self.engine.predict(row, quantiles=self.quantiles)[0]

    def on_second(self, ts: int, spot: dict, fut: dict | None, k_open: float | None = None) -> dict:
        self.push(ts, spot, fut)
        return self.predict(k_open)


# ------------------------------------------------------------------------------------------
def replay(pred: LivePredictor, series: dict, start_i: int, n_steps: int):
    """Drive `pred` second-by-second from a historical `series` (from series.load_range)."""
    ts0 = int(series["start"])
    spot = {k: series[k] for k in SPOT_FIELDS}
    fut = {"fc": series["fc"], "fv": series["fv"], "ftbv": series["ftbv"], "fn": series["fn"]}
    w0 = max(0, start_i - BUF)
    pred.warmup(np.arange(ts0 + w0, ts0 + start_i), {k: v[w0:start_i] for k, v in spot.items()},
                {k: v[w0:start_i] for k, v in fut.items()})
    outs = []
    for i in range(start_i, start_i + n_steps):
        e_next = (ts0 + i + 1) % fe.WIN
        k_open = float(series["o"][i + 1]) if e_next == 0 else None
        outs.append(pred.on_second(ts0 + i, {k: spot[k][i] for k in SPOT_FIELDS},
                                   {k: fut[k][i] for k in FUT_FIELDS}, k_open=k_open))
    return outs


# ------------------------------------------------------------------------------------------
def run_binance(pred: LivePredictor, symbol: str = "BTCUSDT", out_path: str | None = None,
                spot_ws="wss://stream.binance.com:9443/ws", fut_ws="wss://fstream.binance.com/ws",
                rest="https://api.binance.com"):  # pragma: no cover - network
    """Minimal live loop (requires `pip install websocket-client requests`)."""
    import threading

    import requests
    import websocket

    sym = symbol.lower()
    # ---- warm-up: 2 days of spot 1s klines (exact) + futures 1m klines (approximate long windows)
    end = int(time.time()) // 1 * 1000
    start = end - BUF * 1000
    rows = []
    t = start
    while t < end:
        r = requests.get(f"{rest}/api/v3/klines", params=dict(symbol=symbol, interval="1s", startTime=t, limit=1000), timeout=10).json()
        if not r:
            break
        rows += r
        t = r[-1][0] + 1000
    k = np.array(rows, dtype=object)
    ts = (k[:, 0].astype(np.int64) // 1000)
    spot = {"o": k[:, 1].astype(float), "h": k[:, 2].astype(float), "l": k[:, 3].astype(float), "c": k[:, 4].astype(float),
            "v": k[:, 5].astype(float), "qv": k[:, 7].astype(float), "n": k[:, 8].astype(float), "tbv": k[:, 9].astype(float)}
    fr = requests.get("https://fapi.binance.com/fapi/v1/klines", params=dict(symbol=symbol, interval="1m", startTime=start, limit=1500), timeout=10).json()
    fm = {int(x[0]) // 1000: x for x in fr}
    fut = {kk: np.zeros(len(ts)) for kk in FUT_FIELDS}
    for i, tt in enumerate(ts):
        m = fm.get(int(tt) - int(tt) % 60)
        if m is None:
            fut["fc"][i] = np.nan
            continue
        basis = float(m[4]) / float(spot["c"][i])  # minute basis, applied to the spot second
        fut["fc"][i] = spot["c"][i] * basis
        fut["fv"][i] = float(m[5]) / 60; fut["ftbv"][i] = float(m[9]) / 60; fut["fn"][i] = float(m[8]) / 60
    pred.warmup(ts, spot, fut)

    # ---- streaming
    state = {"fut": {}, "spot": None, "k_open": None}
    lock = threading.Lock()

    def on_fut(_, msg):
        d = json.loads(msg)
        sec = int(d["T"]) // 1000
        p, q = float(d["p"]), float(d["q"])
        with lock:
            b = state["fut"].setdefault(sec, {"fc": p, "fv": 0.0, "ftbv": 0.0, "fn": 0.0})
            b["fc"] = p; b["fv"] += q; b["fn"] += 1
            if not d["m"]:
                b["ftbv"] += q

    def emit(out):
        line = json.dumps(out)
        print(line, flush=True)
        if out_path:
            with open(out_path, "a") as f:
                f.write(line + "\n")

    def on_spot(_, msg):
        d = json.loads(msg)["k"]
        sec = int(d["t"]) // 1000
        if state.get("pending_e0") == sec:
            # first print of a new 5-minute window: the reference price K is now known exactly
            state["pending_e0"] = None
            emit(pred.predict(k_open=float(d["o"])))
        if d["x"]:  # kline closed
            bar = {"o": float(d["o"]), "h": float(d["h"]), "l": float(d["l"]), "c": float(d["c"]), "v": float(d["v"]),
                   "qv": float(d["q"]), "n": float(d["n"]), "tbv": float(d["V"])}
            with lock:
                fb = state["fut"].pop(sec, None)
                for old in [s for s in state["fut"] if s < sec]:
                    state["fut"].pop(old)
            pred.push(sec, bar, fb)
            if (sec + 1) % 300 == 0:
                state["pending_e0"] = sec + 1   # wait for the window's first trade to fix K
            else:
                emit(pred.predict())

    wf = websocket.WebSocketApp(f"{fut_ws}/{sym}@aggTrade", on_message=on_fut)
    threading.Thread(target=wf.run_forever, daemon=True).start()
    ws = websocket.WebSocketApp(f"{spot_ws}/{sym}@kline_1s", on_message=on_spot)
    ws.run_forever()
