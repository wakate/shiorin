from invoke import task
from page_generator import PageGenerator


@task
def gen_web(ctx):
    pg = PageGenerator(
        'web_template.html',
        'data/timetable.csv',
        'data/room.csv',
        'data/sponsor.json',
        'web/index.html'
    )
    pg.generate()
