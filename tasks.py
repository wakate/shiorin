from invoke import task
from shiori_generator import ShioriGenerator


@task
def gen_web(ctx):
    sg = ShioriGenerator(
        'data/timetable.csv',
        'data/room.csv',
        'data/sponsor.json',
    )
    sg.generate_web('web_template.html', 'web/index.html')


@task
def gen_paper(ctx):
    sg = ShioriGenerator(
        'data/timetable.csv',
        'data/room.csv',
        'data/sponsor.json',
    )
    sg.generate_paper('paper_template.html', 'paper/index.html')
