#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOG="./logs/cron.log"
HOSTNAME=`hostname`
export CASINO_SETTINGS=~/deployments/config/casino/${HOSTNAME}.py
cd $DIR
source ~/venvs/casino/bin/activate

date >> $LOG
python matchmaker/cron/new_matches.py >> $LOG
