from invoke import task
from shiori_generator import ShioriGenerator


@task
def gen_web(ctx):
    sg = ShioriGenerator(
        'web_template.html',
        'data/timetable.csv',
        'data/room.csv',
        'data/sponsor.json',
    )
    sg.generate_web('web/index.html')
