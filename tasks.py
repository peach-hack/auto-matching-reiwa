import invoke
from invoke import task


@task
def crawl_wakuwaku(c):
    command = "scrapy crawl wakuwaku"
    invoke.run(command)
