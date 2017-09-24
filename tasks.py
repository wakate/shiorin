from invoke import task
from page_generator import PageGenerator


@task
def gen_web(ctx):
    pg = PageGenerator('template.html', 'data.csv', 'room.csv', 'index.html')
    pg.generate()
