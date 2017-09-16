from invoke import run, task
import generator


@task
def gen_web(ctx, filename):
    generator.gen_table(filename)
