"""Replay a historical 5-minute window through the *live* predictor, second by second.

Prints a compact trace of the probabilities through the window and writes the full JSON stream.
usage: python scripts/09_replay_demo.py [--start "2026-10-15 14:30"] [--models artifacts/models]
"""
import argparse
import datetime as dt
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from btcmove import series as se  # noqa: E402
from btcmove.live import BUF, LivePredictor, replay  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--start", default="2026-10-15 14:30")
ap.add_argument("--models", default="artifacts/models")
ap.add_argument("--out", default="artifacts/replay_demo.jsonl")
a = ap.parse_args()

t_win = int(dt.datetime.fromisoformat(a.start).replace(tzinfo=dt.UTC).timestamp())
t_win -= t_win % 300
lo = t_win - BUF - 10
ser = se.load_range(lo, t_win + 400)
pred = LivePredictor.from_artifacts(a.models)
t0 = time.time()
# replay from 1 second before the window so the first emitted decision is e=0
outs = replay(pred, ser, start_i=t_win - lo - 1, n_steps=300)
el = time.time() - t0
with open(a.out, "w") as f:
    for o in outs:
        f.write(json.dumps(o) + "\n")
K = outs[0]["reference_price"]
final = float(ser["c"][t_win - lo + 299])
print(f"window {dt.datetime.fromtimestamp(t_win, dt.UTC):%Y-%m-%d %H:%M} UTC   reference K = {K:.2f}   "
      f"final close = {final:.2f} ({'UP' if final >= K else 'DOWN'})   [{el/len(outs)*1e3:.0f} ms per second]")
print(" e   price      d(bps)  P(close>=K)  P(30s>=K)  P(60s>=K)  sd_close(bps)  P(touch K+10bp)  P(touch K-10bp)")
for o in outs[::15]:
    c = o["horizons"]["close"]
    print(f"{o['elapsed_s']:3d} {o['price']:10.2f} {o['displacement_bps']:7.2f}   {c['p_above_reference']:.3f}      "
          f"{o['horizons']['30s']['p_above_reference']:.3f}      {o['horizons']['60s']['p_above_reference']:.3f}      "
          f"{c['sd_bps']:6.2f}          {c['levels']['K+10bp']['p_touch_before_end']:.3f}            {c['levels']['K-10bp']['p_touch_before_end']:.3f}")
