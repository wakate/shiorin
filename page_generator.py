from jinja2 import Environment, FileSystemLoader
from time_table import TimeTable
from abst_table import AbstTable
from markdown import Markdown
import os


class PageGenerator:
    @staticmethod
    def md_converter(dirname):
        md = Markdown()
        files = os.listdir(dirname)
        htmls = []
        for file in files:
            with open('%s/%s' % (dirname, file), 'r') as f:
                htmls.append(md.convert(f.read()))

        return htmls

    def generate(self, template, page):
        data_dir = 'data'
        t = TimeTable('%s/timetable.csv' % data_dir)
        a = AbstTable('%s/timetable.csv' % data_dir)
        timetable_headings, timetables = t.gen_timetables()
        abst_headings, abst_tables = a.gen_tables()

        env = Environment(loader=FileSystemLoader('./', encoding='utf-8'))
        tmpl = env.get_template(template)
        v = {
            'timetables': timetables,
            'timetable_headings': timetable_headings,
            'abst_headings': abst_headings,
            'abst_tables': abst_tables,
            'info': self.md_converter('info')
        }
        with open(page, 'w') as f:
            f.write(tmpl.render(v))
