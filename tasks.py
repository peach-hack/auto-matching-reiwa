import invoke
from invoke import task


def get_file_name_tokyo(scrapy_name):
    return scrapy_name + "_tokyo.csv"


def get_file_name_kanagawa(scrapy_name):
    return scrapy_name + "_kanagawa.csv"


def get_file_path(file_name):
    RAWDATA_DIR = "./rawdata/"
    return RAWDATA_DIR + file_name


def create_crawl_command(area, days, file_name, scrapy_name):
    return "scrapy crawl -a area={} -a days={} {} -o {}".format(
        area, days, scrapy_name, file_name)


def crawl_base(days, name):
    rawdata_kanagawa = get_file_path(get_file_name_kanagawa(name))
    rawdata_tokyo = get_file_path(get_file_name_tokyo(name))

    try:
        invoke.run('rm {}'.format(rawdata_kanagawa))
        invoke.run('rm {}'.format(rawdata_tokyo))
    except Exception:
        pass
    invoke.run(create_crawl_command("神奈川県", days, name, rawdata_kanagawa))
    invoke.run(create_crawl_command("東京都", days, name, rawdata_tokyo))


@task
def crawl_wakuwaku(c, days):
    name = "wakuwaku"
    crawl_base(days, name)


@task
def crawl_happymail(c, days):
    name = "happymail"
    crawl_base(days, name)


@task
def crawl_pcmax(c, days):
    name = "pcmax"
    crawl_base(days, name)


@task
def crawl_ikukuru(c, days):
    name = "ikukuru"
    crawl_base(days, name)
