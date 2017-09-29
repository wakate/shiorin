from jinja2 import Environment, FileSystemLoader
from time_table import TimeTable
from abst_table import AbstTable
from room import Room
from markdown import Markdown
import json
import os


class ShioriGenerator:
    def __init__(self, timetable_csv, room_csv, sponsor_json):
        self.timetable_source_file = timetable_csv
        self.room_source_file = room_csv
        self.sponsor_source_file = sponsor_json

    @staticmethod
    def md_converter(dirname):
        md = Markdown()
        files = os.listdir('md/%s' % dirname)
        htmls = []
        for file in files:
            with open('md/%s/%s' % (dirname, file), 'r') as f:
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

    @staticmethod
    def gen_sponsor_table_2(filename):
        with open(filename, 'r') as f:
            sp = json.load(f)
        sp1 = {
            'logo': sp['logo'][0:2],
            'name': sp['name'][0:2],
        }
        sp2 = {
            'logo': sp['logo'][2:4],
            'name': sp['name'][2:4]
        }
        sponsor = [
            list(map(lambda x: '<td><img src="%s"></td>' % x, sp1['logo'])),
            list(map(lambda x: '<td>%s 様</td>' % x, sp1['name'])),
            list(map(lambda x: '<td><img src="%s"></td>' % x, sp2['logo'])),
            list(map(lambda x: '<td>%s 様</td>' % x, sp2['name'])),
        ]
        return sponsor

    def generate_web(self, template, output):
        t = TimeTable(self.timetable_source_file)
        timetable_headings, timetables = t.gen_tables()

        a = AbstTable(self.timetable_source_file)
        abst_headings, abst_tables = a.gen_tables()

        r = Room(self.room_source_file)
        room_headings, room_tables = r.gen_room_table_t()

        env = Environment(loader=FileSystemLoader('./', encoding='utf-8'))
        tmpl = env.get_template(template)
        v = {
            'timetables': timetables,
            'timetable_headings': timetable_headings,
            'abst_headings': abst_headings,
            'abst_tables': abst_tables,
            'info': self.md_converter('info'),
            'room_headings': room_headings,
            'room_tables': room_tables,
            'sponsor': self.gen_sponsor_table(self.sponsor_source_file),
            'ryokan': self.md_converter('ryokan')
        }
        with open(output, 'w') as f:
            f.write(tmpl.render(v))

    def generate_paper(self, template, output):
        t = TimeTable(self.timetable_source_file)
        timetable_headings, timetables = t.gen_paper_table()

        r = Room(self.room_source_file)
        room_headings, room_tables = r.gen_room_table()

        env = Environment(loader=FileSystemLoader('./', encoding='utf-8'))
        tmpl = env.get_template(template)
        v = {
            'timetable_headings': timetable_headings,
            'timetables': timetables,
            'room_headings': room_headings,
            'room_tables': room_tables,
            'sponsor': self.gen_sponsor_table_2(self.sponsor_source_file),
            'info': self.md_converter('paper_info')
        }
        with open(output, 'w') as f:
            f.write(tmpl.render(v))
