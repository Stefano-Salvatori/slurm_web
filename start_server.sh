#!/bin/bash
#export LC_ALL=C.UTF-8
#export LANG=C.UTF-8

# sudo -u munge munged

eval "$(conda shell.bash hook)"
conda activate slurm_web

export FLASK_APP=flaskr

MODE="${1:-dev}"
PORT="${2:-37336}"

if [[ "$MODE" == "dev" ]]
then
    export FLASK_ENV=development
    flask run --host=0.0.0.0 --port=$PORT
elif [[ "$MODE" == "prod" ]]
then
    export FLASK_ENV=production
    waitress-serve --port=$PORT --call 'flaskr:create_app'
else
    echo "First argument must be one of 'dev' or 'prod'"
fi

