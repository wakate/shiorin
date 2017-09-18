from invoke import task
from page_generator import PageGenerator
from abst_table import AbstTable


@task
def gen_web(ctx):
    pg = PageGenerator
    pg.generate('template.html', 'hoge.html')


@task
def gen_abst_table(ctx):
    at = AbstTable('data.csv')
    at.gen_tables()
