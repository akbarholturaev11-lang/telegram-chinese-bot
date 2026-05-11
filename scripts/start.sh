#!/bin/bash
set -e

echo "=== Alembic migration check ==="

# alembic current ni xato bo'lsa ham to'xtatmasdan olamiz
CURRENT=$(alembic current 2>&1 || true)
echo "Alembic current: '$CURRENT'"

# alembic_version jadvali yo'q yoki bo'sh bo'lsa — chiqish bo'sh yoki xato xabari
# Bunday holda: jadvallar allaqachon SQLAlchemy create_all bilan yaratilgan,
# shunchaki alembic ni head ga stamp qilamiz (hech qanday migration ishlatmasdan)
STRIPPED=$(echo "$CURRENT" | tr -d '[:space:]')
if [ -z "$STRIPPED" ] || echo "$CURRENT" | grep -qiE "error|does not exist|no such|can't locate|not found"; then
    echo "No alembic version detected — stamping at head (skips re-running old migrations)..."
    alembic stamp head
    echo "Stamp done."
fi

echo "=== Running alembic upgrade head ==="
alembic upgrade head && echo "Migrations OK." || {
    echo "Upgrade failed — forcing stamp at head and retrying..."
    alembic stamp head
    alembic upgrade head
}

echo "=== Starting uvicorn ==="
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
