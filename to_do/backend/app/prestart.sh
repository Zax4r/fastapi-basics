#!/bin/sh
set -e

echo "Run apply migrations.."
alembic -c /app/app/alembic.ini upgrade head
echo "Migrations applied!"

exec "$@"