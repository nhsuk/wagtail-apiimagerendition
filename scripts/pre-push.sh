#!/usr/bin/env sh

echo "Running pre-push hook"
docker-compose run --rm web python manage.py test --no-input

# $? stores exit value of the last command
if [ $? -ne 0 ]; then
    echo "Unittest must pass before commit!"
    exit 1
fi

echo "Unitest - Passed"