#!/usr/bin/env bash
# Production refit: same recipe as the evaluated model, but trained on all data up to the last two months,
# which are used for early stopping; then the live recalibrator is initialised on the final 14 days.
# The *expected* performance of this model is the one measured out-of-sample for artifacts/models.
set -e
cd "$(dirname "$0")/.."
END=${END:-2026-11-03}
VAL=${VAL:-2026-09-01}
python scripts/03_train.py --frac ${FRAC:-0.35} --dates 2024-02-01,$VAL,$END,$END --out artifacts/production
python scripts/10_fit_recal.py --models artifacts/production --end $END
