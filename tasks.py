import invoke
from invoke import task


@task
def crawl_wakuwaku(c):
    file_path = "./rawdata/wakuwaku.csv"
    command = "rm {} && scrapy crawl wakuwaku -o {}".format(
        file_path, file_path)
    invoke.run(command)
