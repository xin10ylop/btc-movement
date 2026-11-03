#!/usr/bin/env bash
# Background chain: ablations (val only) -> sequence CNN (val only) -> walk-forward folds.
cd "$(dirname "$0")/.."
for H in 30 60 T; do python scripts/05_ablation.py --horizon $H --frac 0.15 > artifacts/ablation_$H.out 2>&1; done
python scripts/06_sequence_model.py --horizon 30 --frac 0.08 > artifacts/seq_30.out 2>&1
python scripts/06_sequence_model.py --horizon T --frac 0.08 > artifacts/seq_T.out 2>&1
FRAC=0.3 bash scripts/07_walkforward.sh
echo ALLDONE > artifacts/experiments.done
