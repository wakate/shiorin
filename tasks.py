from invoke import task
from page_generator import PageGenerator
from room import Room


@task
def gen_web(ctx):
    pg = PageGenerator()
    pg.generate('template.html', 'hoge.html')


@task
def test_room(ctx):
    r = Room('data/room.csv')
    r.gen_room_table()
