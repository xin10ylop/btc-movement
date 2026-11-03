#!/usr/bin/env bash
# After the 10s/15s models are trained: independent val/test evaluation, live recalibration init, regime slices.
cd "$(dirname "$0")/.."
until [ -f artifacts/models_v2/horizon_15.pkl ] && grep -q "\[15\] saved" artifacts/models_v2/train.log; do sleep 30; done
until [ -f artifacts/models_v2/report_test.json ]; do sleep 30; done   # main v2 test eval written first
python scripts/04_evaluate.py --split val --horizons 10,15 --models artifacts/models_v2 --qsub 30000 --boot 300 > artifacts/eval_v2_short_val.out 2>&1
python scripts/04_evaluate.py --split test --horizons 10,15 --models artifacts/models_v2 --qsub 60000 --boot 1000 > artifacts/eval_v2_short_test.out 2>&1
python scripts/10_fit_recal.py --models artifacts/models_v2 > artifacts/recal_v2.out 2>&1
python scripts/14_regime_eval.py --models artifacts/models_v2 --split test > artifacts/regime_eval_v2_all.out 2>&1
echo DONE > artifacts/short_chain.done
