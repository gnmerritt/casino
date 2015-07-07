#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HOST_IP=`ifconfig eth0 | awk '/t addr:/{gsub(/.*:/,"",$2);print$2}'`
CPUS=`grep -c ^processor /proc/cpuinfo`
JOBS=$(($CPUS - 1))
HOSTNAME=`hostname`
cd $DIR
source ~/venvs/casino/bin/activate
export CASINO_SETTINGS=~/deployments/config/casino/${HOSTNAME}.py
export CASINO_OAUTH=~/deployments/config/casino/oauth.py
gunicorn matchmaker:app \
    -b ${HOST_IP}:8000 \
    -w $JOBS
