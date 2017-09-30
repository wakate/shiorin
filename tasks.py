from invoke import task
from shiori_generator import ShioriGenerator
import os


@task
def gen_web(ctx):
    sg = ShioriGenerator(
        'data/timetable.csv',
        'data/room.csv',
        'data/sponsor.json',
    )
    sg.generate_web('templates/web/template.html', 'web/index.html')


@task
def gen_paper(ctx):
    sg = ShioriGenerator(
        'data/timetable.csv',
        'data/room.csv',
        'data/sponsor.json',
    )
    templates_dir = os.path.join('templates', 'paper')
    templates = {
        'cover': os.path.join(templates_dir, 'cover.html'),
        'timetable': os.path.join(templates_dir, 'timetable.html'),
        'room': os.path.join(templates_dir, 'room.html'),
        'ryokan': os.path.join(templates_dir, 'ryokan.html'),
        'info': os.path.join(templates_dir, 'info.html')
    }
    sg.generate_paper(templates, 'paper')
