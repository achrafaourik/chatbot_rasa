#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "Starting makemigrations"
python manage.py flush --no-input
python manage.py makemigrations
echo "Finished makemigrations"

echo "Starting migrate"
python manage.py migrate
echo "Finished migrate"

echo "Starting Rasa Train model"
rasa train
echo "Finised Rasa Train"

rasa run -m models --enable-api --cors "*" --debug & rasa run actions &

exec "$@"