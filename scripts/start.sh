#!/bin/bash
set -e

echo "=== Alembic migration check ==="

# alembic current ishlamasas (alembic_version yo'q yoki xato) — stamp head
CURRENT=$(alembic current 2>&1 || true)
echo "Current state: $CURRENT"

if echo "$CURRENT" | grep -qiE "error|does not exist|no such|relation.*not found|can't locate"; then
    echo "alembic_version not found. Stamping DB at head (tables already exist)..."
    alembic stamp head
elif echo "$CURRENT" | grep -q "(head)"; then
    echo "Already at head. No migration needed."
else
    echo "Running alembic upgrade head..."
fi

# Bu safar xatodan qat'iy nazar upgrade ishlatamiz (no-op bo'lsa ham xavfsiz)
alembic upgrade head

echo "=== Starting uvicorn ==="
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
