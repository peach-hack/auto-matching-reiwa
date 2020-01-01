import invoke
from invoke import task


@task
def crawl_wakuwaku(c):
    command = "scrapy crawl wakuwaku -o ./rawdata/wakuwaku.csv"
    invoke.run(command)
