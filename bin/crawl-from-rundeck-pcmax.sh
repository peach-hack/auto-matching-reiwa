#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate auto-matching

HOMEDIR=${HOME}/repo/auto-matching-reiwa

cd ${HOMEDIR}

AREA_TOKYO="東京都"
AREA_KANAGAWA="神奈川県"

scrapy crawl -a area=${AREA_TOKYO} -a days=1 pcmax --loglevel=INFO
scrapy crawl -a area=${AREA_KANAGAWA} -a days=1 pcmax --loglevel=INFO
