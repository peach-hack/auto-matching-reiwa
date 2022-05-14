# Auto Matching(令和版)

![](https://img.shields.io/github/issues/peach-hack/auto-matching-reiwa.svg)
[![Open Source Love](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](https://github.com/peach-hack/auto-matching-reiwa/)

* Pyhton 3.7.4
* Scrapy 1.6.0
* MySQL 8.0.18

## 概要

統合出会い系エンジン(IDE: Integreted Deai Engine).

出会い系マッチングサイトを AI、データ分析、自動化を駆使してハッキングします。[Auto Matching](https://github.com/peach-hack/auto-matching)のリメイクです。今回はPythonとSQLをつかっています。

とりあえずスクレイピングしてきたデータをローカルのMySQLに入れて、SQLによるサクラ判定を実装してみました。大体1日に8000レコードずつ溜まっていきますが、サクラ判定をかけると100レコードくらいまで絞り込めます。出会い系サイトの9割の投稿はクズという話はよくききますが、5%の宝を如何にして見つけ出すかが勝負だと思います。

* https://github.com/peach-hack/auto-matching-reiwa/blob/master/sql/sakura_analysis.sql

1時間に1度定期実行をかけてクローリングをしています。cronをつかっていたけど、Rundeckといういいツールをみつけたので、こちらで運用中。

Tinderはモチベーションが高まったら対応します。

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
