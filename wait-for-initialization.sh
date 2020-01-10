#! /bin/bash

set -o errexit
set -o pipefail
cmd="$@"

function postgres_ready(){
python3 << END
import sys
import psycopg2
import environs
try:
    env = environs.Env()
    dbname = env.str('POSTGRES_DB')
    user = env.str('POSTGRES_USER')
    password = env.str('POSTGRES_PASSWORD')
    host = env.str('POSTGRES_HOST')
    port = env.str('POSTGRES_PORT')
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Migrating..."
python manage.py migrate

>&2 echo "Collect static..."
python manage.py collectstatic --noinput


>&2 echo "Starting Gunicorn..."
    exec gunicorn birds.wsgi:application \
      -k egg:meinheld#gunicorn_worker \
      --name birds --bind 0.0.0.0:8000 --workers 3 \
      "$@"
