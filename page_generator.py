from jinja2 import Environment, FileSystemLoader
from time_table import TimeTable
from abst_table import AbstTable
from room import Room
from markdown import Markdown
import json
import os


class PageGenerator:
    def __init__(self, template_html, timetable_csv, room_csv, sponsor_json, output):
        self.template_html = template_html
        self.timetable_source_file = timetable_csv
        self.room_source_file = room_csv
        self.sponsor_source_file = sponsor_json
        self.page_html = output

    @staticmethod
    def md_converter(dirname):
        md = Markdown()
        files = os.listdir(dirname)
        htmls = []
        for file in files:
            with open('%s/%s' % (dirname, file), 'r') as f:
                htmls.append(md.convert(f.read()))

        return htmls

    @staticmethod
    def gen_sponsor_table(filename):
        with open(filename, 'r') as f:
            sp = json.load(f)
        sponsor = [
            list(map(lambda x: '<td><img src="%s"></td>' % x, sp['logo'])),
            list(map(lambda x: '<td>%s 様(1口)</td>' % x, sp['name']))
        ]

        return sponsor

    def generate(self):
        t = TimeTable(self.timetable_source_file)
        timetable_headings, timetables = t.gen_timetables()

        a = AbstTable(self.timetable_source_file)
        abst_headings, abst_tables = a.gen_tables()

        r = Room(self.room_source_file)
        room_headings, room_tables = r.gen_room_table()

        sponsor = self.gen_sponsor_table(self.sponsor_source_file)

        env = Environment(loader=FileSystemLoader('./', encoding='utf-8'))
        tmpl = env.get_template(self.template_html)
        v = {
            'timetables': timetables,
            'timetable_headings': timetable_headings,
            'abst_headings': abst_headings,
            'abst_tables': abst_tables,
            'info': self.md_converter('info'),
            'room_headings': room_headings,
            'room_tables': room_tables,
            'sponsor': sponsor
        }
        with open(self.page_html, 'w') as f:
            f.write(tmpl.render(v))
