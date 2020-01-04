#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate auto-matching

HOMEDIR=${HOME}/repo/auto-matching-reiwa
LOGDIR="${HOMEDIR}/log"

LOGFILE_WAKUWAKU_TOKYO=wakuwaku_tokyo.log
LOGFILE_WAKUWAKU_KANAGAWA=wakuwaku_kanagawa.log
LOGFILE_IKUKURU_TOKYO=ikukuru_tokyo.log
LOGFILE_IKUKURU_KANAGAWA=ikukuru_kanagawa.log

LOGPATH_WAKUWAKU_TOKYO="${LOGDIR}/${LOGFILE_WAKUWAKU_TOKYO}"
LOGPATH_WAKUWAKU_KANAGAWA="${LOGDIR}/${LOGFILE_WAKUWAKU_KANAGAWA}"
LOGPATH_IKUKURU_TOKYO="${LOGDIR}/${LOGFILE_IKUKURU_TOKYO}"
LOGPATH_IKUKURU_KANAGAWA="${LOGDIR}/${LOGFILE_IKUKURU_KANAGAWA}"

cd ${HOMEDIR}

rm -f ${LOGPATH_WAKUWAKU_TOKYO}
rm -f ${LOGPATH_WAKUWAKU_KANAGAWA}
rm -f ${LOGPATH_IKUKURU_TOKYO}
rm -f ${LOGPATH_IKUKURU_KANAGAWA}

AREA_TOKYO="東京都"
AREA_KANAGAWA="神奈川県"

scrapy crawl -a area=${AREA_TOKYO} -a days=1 wakuwaku --logfile=${LOGPATH_WAKUWAKU_TOKYO} --loglevel=INFO
scrapy crawl -a area=${AREA_KANAGAWA} -a days=1 wakuwaku --logfile=${LOGPATH_WAKUWAKU_KANAGAWA} --loglevel=INFO
scrapy crawl -a area=${AREA_TOKYO} -a days=1 ikukuru --logfile=${LOGPATH_IKUKURU_TOKYO} --loglevel=INFO
scrapy crawl -a area=${AREA_KANAGAWA} -a days=1 ikukuru --logfile=${LOGPATH_IKUKURU_KANAGAWA} --loglevel=INFO
