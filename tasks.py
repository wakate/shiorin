from invoke import task
from page_generator import PageGenerator


@task
def gen_web(ctx):
    pg = PageGenerator
    pg.generate('template.html', 'hoge.html')
