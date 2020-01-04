# Auto Matching(令和版)

![](https://img.shields.io/github/issues/peach-hack/auto-matching-reiwa.svg)
[![Open Source Love](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](https://github.com/peach-hack/auto-matching-reiwa/)

* Pyhton 3.7.4
* Scrapy 1.6.0
* MySQL 8.0.18

## 概要

統合出会い系エンジン(IDE: Integreted Deai Engine).

出会い系マッチングサイトを AI、データ分析、自動化を駆使してハッキングします。[Auto Matching](https://github.com/peach-hack/auto-matching)のリメイクです。今回はPythonとSQLをつかっています。

とりあえずスクレイピングしてきたデータをローカルのMySQLに入れて、SQLによるサクラ判定を実装してみました。大体1日に8000レコードずつ溜まっていきますが、サクラ判定をかけると300レコードくらいまで絞り込めます。

* https://github.com/peach-hack/auto-matching-reiwa/blob/master/sql/sakura_analysis.sql

1時間に1度定期実行をかけてクローリングをしている。cronをつかっていたけど、Rundeckといういいツールをみつけたので、こちらで運用中。

Tinderはモチベーションが高まったら対応します。

### 対応サイト

- [ハッピーメール](https://happymail.co.jp/?af14212217)
- [ワクワクメール](https://550909.com/?f6858637)
- [PCMAX](https://pcmax.jp/lp/?ad_id=rm181904)
- [イククル](https://194964.com/AF1213451)
- [ミントC!Jメール](https://mintj.com/?mdc=991&afguid=1iojxazbuotgo2d2n8pf4xszii)
- [メルパラ](https://meru-para.com/?mdc=991&afguid=1y803u9dpjvt42admh2jxq7tv6)

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
