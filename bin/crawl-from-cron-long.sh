#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate auto-matching

HOMEDIR=${HOME}/repo/auto-matching-reiwa
LOGDIR="${HOMEDIR}/log"

LOGFILE_HAPPYMAIL_TOKYO=happymail_tokyo.log
LOGFILE_HAPPYMAIL_KANAGAWA=happymail_kanagawa.log
LOGFILE_PCMAX_TOKYO=pcmax_tokyo.log
LOGFILE_PCMAX_KANAGAWA=pcmax_kanagawa.log

LOGPATH_HAPPYMAIL_TOKYO="${LOGDIR}/${LOGFILE_HAPPYMAIL_TOKYO}"
LOGPATH_HAPPYMAIL_KANAGAWA="${LOGDIR}/${LOGFILE_HAPPYMAIL_KANAGAWA}"
LOGPATH_PCMAX_TOKYO="${LOGDIR}/${LOGFILE_PCMAX_TOKYO}"
LOGPATH_PCMAX_KANAGAWA="${LOGDIR}/${LOGFILE_PCMAX_KANAGAWA}"

cd ${HOMEDIR}

rm -f ${LOGPATH_HAPPYMAIL_TOKYO}
rm -f ${LOGPATH_HAPPYMAIL_KANAGAWA}
rm -f ${LOGPATH_PCMAX_TOKYO}
rm -f ${LOGPATH_PCMAX_KANAGAWA}

AREA_TOKYO="東京都"
AREA_KANAGAWA="神奈川県"

scrapy crawl -a area=${AREA_TOKYO} -a days=1 happymail --logfile=${LOGPATH_HAPPYMAIL_TOKYO} --loglevel=INFO
scrapy crawl -a area=${AREA_KANAGAWA} -a days=1 happymail --logfile=${LOGPATH_HAPPYMAIL_KANAGAWA} --loglevel=INFO
scrapy crawl -a area=${AREA_TOKYO} -a days=1 pcmax --logfile=${LOGPATH_PCMAX_TOKYO} --loglevel=INFO
scrapy crawl -a area=${AREA_KANAGAWA} -a days=1 pcmax --logfile=${LOGPATH_PCMAX_KANAGAWA} --loglevel=INFO
