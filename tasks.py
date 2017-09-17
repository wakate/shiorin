from invoke import task
import generator


@task
def gen_web(ctx, timetable):
    generator.gen_page(timetable, 'template.html', 'hoge.html')
