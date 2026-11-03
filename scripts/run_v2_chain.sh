#!/usr/bin/env bash
# After v2 training: evaluations, regime slices, walk-forward (v2 recipe), remaining experiments.
cd "$(dirname "$0")/.."
until [ -f artifacts/models_v2/horizon_T.pkl ]; do sleep 30; done
python scripts/04_evaluate.py --split val --models artifacts/models_v2 --qsub 30000 --boot 300 > artifacts/eval_v2_val.out 2>&1
python scripts/04_evaluate.py --split test --models artifacts/models_v2 --qsub 60000 --boot 1000 > artifacts/eval_v2_test.out 2>&1
python scripts/14_regime_eval.py --models artifacts/models_v2 --split test > artifacts/regime_eval_v2.out 2>&1
FRAC=0.3 bash scripts/07_walkforward.sh
python scripts/05_ablation.py --horizon T --frac 0.15 > artifacts/ablation_T.out 2>&1
python scripts/06_sequence_model.py --horizon 30 --frac 0.08 --models artifacts/models_v2 > artifacts/seq_30.out 2>&1
echo ALLDONE > artifacts/v2_chain.done
