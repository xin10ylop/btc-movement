#!/usr/bin/env bash
# Walk-forward: retrain the full stack on expanding windows and evaluate on later, disjoint test periods.
# Fold A: test May-Aug 2025 ; Fold B: test Nov 2025 - Feb 2026 ; main run: test Jun - Oct 2026.
set -e
cd "$(dirname "$0")/.."
FRAC=${FRAC:-0.3}
run() {  # name dates
  python scripts/03_train.py --frac "$FRAC" --dates "$2" --out "artifacts/wf_$1" > "artifacts/wf_$1.out" 2>&1
  python scripts/04_evaluate.py --split test --dates "$2" --models "artifacts/wf_$1" --qsub 30000 --boot 300 > "artifacts/wf_$1_eval.out" 2>&1
}
run A 2024-02-01,2025-03-01,2025-05-01,2025-09-01
run B 2024-02-01,2025-09-01,2025-11-01,2026-03-01
