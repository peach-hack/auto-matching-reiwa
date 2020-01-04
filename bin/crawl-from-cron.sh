#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate auto-matching

HOMEDIR=${HOME}/repo/auto-matching-reiwa
LOGDIR="${HOMEDIR}/log"

LOGFILE_WAKUWAKU_TOKYO=wakuwaku_tokyo.log
LOGFILE_WAKUWAKU_KANAGAWA=wakuwaku_kanagawa.log
LOGFILE_IKUKURU_TOKYO=ikukuru_tokyo.log
LOGFILE_IKUKURU_KANAGAWA=ikukuru_kanagawa.log
LOGFILE_HAPPYMAIL_TOKYO=happymail_tokyo.log
LOGFILE_HAPPYMAIL_KANAGAWA=happymail_kanagawa.log
LOGFILE_PCMAX_TOKYO=pcmax_tokyo.log
LOGFILE_PCMAX_KANAGAWA=pcmax_kanagawa.log
LOGFILE_MINT_TOKYO=mint_tokyo.log
LOGFILE_MINT_KANAGAWA=mint_kanagawa.log
LOGFILE_MERUPARA_TOKYO=merupara_tokyo.log
LOGFILE_MERUPARA_KANAGAWA=merupara_kanagawa.log

LOGPATH_WAKUWAKU_TOKYO="${LOGDIR}/${LOGFILE_WAKUWAKU_TOKYO}"
LOGPATH_WAKUWAKU_KANAGAWA="${LOGDIR}/${LOGFILE_WAKUWAKU_KANAGAWA}"
LOGPATH_IKUKURU_TOKYO="${LOGDIR}/${LOGFILE_IKUKURU_TOKYO}"
LOGPATH_IKUKURU_KANAGAWA="${LOGDIR}/${LOGFILE_IKUKURU_KANAGAWA}"
LOGPATH_HAPPYMAIL_TOKYO="${LOGDIR}/${LOGFILE_HAPPYMAIL_TOKYO}"
LOGPATH_HAPPYMAIL_KANAGAWA="${LOGDIR}/${LOGFILE_HAPPYMAIL_KANAGAWA}"
LOGPATH_PCMAX_TOKYO="${LOGDIR}/${LOGFILE_PCMAX_TOKYO}"
LOGPATH_PCMAX_KANAGAWA="${LOGDIR}/${LOGFILE_PCMAX_KANAGAWA}"
LOGPATH_MINT_TOKYO="${LOGDIR}/${LOGFILE_MINT_TOKYO}"
LOGPATH_MINT_KANAGAWA="${LOGDIR}/${LOGFILE_MINT_KANAGAWA}"
LOGPATH_MERUPARA_TOKYO="${LOGDIR}/${LOGFILE_MERUPARA_TOKYO}"
LOGPATH_MERUPARA_KANAGAWA="${LOGDIR}/${LOGFILE_MERUPARA_KANAGAWA}"


cd ${HOMEDIR}

rm -f ${LOGPATH_WAKUWAKU_TOKYO}
rm -f ${LOGPATH_WAKUWAKU_KANAGAWA}
rm -f ${LOGPATH_IKUKURU_TOKYO}
rm -f ${LOGPATH_IKUKURU_KANAGAWA}
rm -f ${LOGPATH_HAPPYMAIL_TOKYO}
rm -f ${LOGPATH_HAPPYMAIL_KANAGAWA}
rm -f ${LOGPATH_PCMAX_TOKYO}
rm -f ${LOGPATH_PCMAX_KANAGAWA}
rm -f ${LOGPATH_MINT_TOKYO}
rm -f ${LOGPATH_MINT_KANAGAWA}
rm -f ${LOGPATH_MERUPARA_TOKYO}
rm -f ${LOGPATH_MERUPARA_KANAGAWA}

AREA_TOKYO="東京都"
AREA_KANAGAWA="神奈川県"

scrapy crawl -a area=${AREA_TOKYO} -a days=1 wakuwaku --logfile=${LOGPATH_WAKUWAKU_TOKYO} --loglevel=INFO
scrapy crawl -a area=${AREA_KANAGAWA} -a days=1 wakuwaku --logfile=${LOGPATH_WAKUWAKU_KANAGAWA} --loglevel=INFO
scrapy crawl -a area=${AREA_TOKYO} -a days=1 ikukuru --logfile=${LOGPATH_IKUKURU_TOKYO} --loglevel=INFO
scrapy crawl -a area=${AREA_KANAGAWA} -a days=1 ikukuru --logfile=${LOGPATH_IKUKURU_KANAGAWA} --loglevel=INFO
scrapy crawl -a area=${AREA_TOKYO} -a days=1 happymail --logfile=${LOGPATH_HAPPYMAIL_TOKYO} --loglevel=INFO
scrapy crawl -a area=${AREA_KANAGAWA} -a days=1 happymail --logfile=${LOGPATH_HAPPYMAIL_KANAGAWA} --loglevel=INFO
scrapy crawl -a area=${AREA_TOKYO} -a days=1 pcmax --logfile=${LOGPATH_PCMAX_TOKYO} --loglevel=INFO
scrapy crawl -a area=${AREA_KANAGAWA} -a days=1 pcmax --logfile=${LOGPATH_PCMAX_KANAGAWA} --loglevel=INFO
scrapy crawl -a area=${AREA_TOKYO} -a days=1 mint --logfile=${LOGPATH_MINT_TOKYO} --loglevel=INFO
scrapy crawl -a area=${AREA_KANAGAWA} -a days=1 mint --logfile=${LOGPATH_MINT_KANAGAWA} --loglevel=INFO
scrapy crawl -a area=${AREA_TOKYO} -a days=1 merupara --logfile=${LOGPATH_MERUPARA_TOKYO} --loglevel=INFO
scrapy crawl -a area=${AREA_KANAGAWA} -a days=1 merupara --logfile=${LOGPATH_MERUPARA_KANAGAWA} --loglevel=INFO
