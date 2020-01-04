# Auto Matching(令和版)

![](https://img.shields.io/github/issues/peach-hack/auto-matching-reiwa.svg)
[![Open Source Love](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](https://github.com/peach-hack/auto-matching-reiwa/)

* Pyhton 3.7.4
* Scrapy 1.6.0
* MySQL 8.0.18

## 概要

令和版統合出会い系エンジン(IDE: Integreted Deai Engine).

出会い系マッチングサイトを AI、データ分析、自動化を駆使してハッキングする Web アプリです。平成の伝説のアプリ、[Auto Matching](https://github.com/peach-hack/auto-matching)を令和の時代に再定義し、一から再構築します。

今回は、とりあえずスクレイピングしてきたデータをローカルのMySQLに入れて、SQLによるサクラ判定を実装してみました。サービス化は余裕があればやります。

* https://github.com/peach-hack/auto-matching-reiwa/blob/master/sql/sakura_analysis.sql

Tinderはモチベーションが高まったら対応します。

### 対応サイト

- [ハッピーメール](https://happymail.co.jp/?af14212217)
- [ワクワクメール](https://550909.com/?f6858637)
- [PCMAX](https://pcmax.jp/lp/?ad_id=rm181904)
- [イククル](https://194964.com/AF1213451)

## 新規環境構築

最低限入れておくものを列挙しておく。

* scrapy
* selenium(pip)
* python-dotenv(pip)
* invoke
* numpy
* pandas
* seaborn
* matplotlib
* flake8
* yapf
* mysqlclient
* alembic
* sqlalchemy

## 出会い系大手４サイトの統計データ分析

ハッピーメール, ワクワクメール, PCMAX, イククルの4サイトのデータ分析。
* https://github.com/peach-hack/auto-matching-reiwa/blob/master/notebooks/data-analysis.ipynb
