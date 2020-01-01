import invoke
from invoke import task

RAWDATA_WAKUWAKU = "./rawdata/wakuwaku.csv"


def create_crawl_wakuwaku_command(area, days):
    return "scrapy crawl -a area={} -a days={} wakuwaku -o {}".format(
        area, days, RAWDATA_WAKUWAKU)


@task
def crawl_wakuwaku(c, days):
    try:
        invoke.run('rm {}'.format(RAWDATA_WAKUWAKU))
    except Exception:
        pass
    invoke.run(create_crawl_wakuwaku_command("神奈川県", days))
    invoke.run(create_crawl_wakuwaku_command("東京都", days))
