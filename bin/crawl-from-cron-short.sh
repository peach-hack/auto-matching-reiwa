#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate auto-matching

cd /home/tsu-nera/repo/auto-matching-reiwa

# with scroll
scrapy crawl -a area="東京都" -a days=1 happymail --nolog
scrapy crawl -a area="神奈川県" -a days=1 happymail --nolog
scrapy crawl -a area="東京都" -a days=1 pcmax --nolog
scrapy crawl -a area="神奈川県" -a days=1 pcmax --nolog
