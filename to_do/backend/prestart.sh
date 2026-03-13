#!/bin/sh
set -e

echo "Run apply migrations.."
alembic -c /app/alembic.ini upgrade head
echo "Migrations applied!"

exec "$@"