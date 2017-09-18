from jinja2 import Environment, FileSystemLoader
from time_table import TimeTable
from abst_table import AbstTable


class PageGenerator:
    @staticmethod
    def generate(template, page):
        t = TimeTable('data.csv')
        a = AbstTable('data.csv')
        timetable_headings, timetables = t.gen_timetables()
        abst_headings, abst_tables = a.gen_tables()

        env = Environment(loader=FileSystemLoader('./', encoding='utf-8'))
        tmpl = env.get_template(template)
        v = {
            'timetables': timetables,
            'timetable_headings': timetable_headings,
            'abst_headings': abst_headings,
            'abst_tables': abst_tables
        }
        with open(page, 'w') as f:
            f.write(tmpl.render(v))
