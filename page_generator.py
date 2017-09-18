from jinja2 import Environment, FileSystemLoader
from time_table import TimeTable


class PageGenerator:
    @staticmethod
    def generate(template, page):
        t = TimeTable('data.csv')
        timetable_headings, timetables = t.gen_timetables()

        env = Environment(loader=FileSystemLoader('./', encoding='utf-8'))
        tmpl = env.get_template(template)
        v = {
            'timetables': timetables,
            'timetable_headings': timetable_headings
        }
        with open(page, 'w') as f:
            f.write(tmpl.render(v))
