import invoke
from invoke import task

RAWDATA_WAKUWAKU_TOKYO = "./rawdata/wakuwaku_tokyo.csv"
RAWDATA_WAKUWAKU_KANAGAWA = "./rawdata/wakuwaku_kanagawa.csv"


def create_crawl_wakuwaku_command(area, days, file_name):
    return "scrapy crawl -a area={} -a days={} wakuwaku -o {}".format(
        area, days, file_name)


@task
def crawl_wakuwaku(c, days):
    try:
        invoke.run('rm {}'.format(RAWDATA_WAKUWAKU_KANAGAWA))
        invoke.run('rm {}'.format(RAWDATA_WAKUWAKU_TOKYO))
    except Exception:
        pass
    invoke.run(
        create_crawl_wakuwaku_command("神奈川県", days, RAWDATA_WAKUWAKU_KANAGAWA))
    invoke.run(
        create_crawl_wakuwaku_command("東京都", days, RAWDATA_WAKUWAKU_TOKYO))
