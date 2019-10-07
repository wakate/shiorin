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
        sponsor_source_file = sponsor_json
        with open(sponsor_source_file, 'r') as f:
            sp = json.load(f)
        self.normal_sponsor = sp['normal']
        self.party_sponsor = sp['party']

    @staticmethod
    def md_converter(dirname):
        md = Markdown()
        files = os.listdir('md/%s' % dirname)
        htmls = []
        for file in files:
            if not file.endswith(".md"):
                continue

            with open('md/%s/%s' % (dirname, file), 'r') as f:
                htmls.append(md.convert(f.read()))

        return htmls

    @staticmethod
    def gen_sponsor_table(config):
        sponsor = [
            list(map(lambda x: '<td><img src="%s"></td>' % x, config['logo'])),
            list(map(lambda x: '<td>%s 様<br>(1口)</td>' % x, config['name']))
        ]
        return sponsor

    @staticmethod
    def gen_sponsor_table_alt(config):
        sponsor = [
            list(map(lambda x: '<td><img src="%s"></td>' % x, config['logo'])),
            list(map(lambda x: '<td>%s 様</td>' % x, config['name'])),
        ]
        return sponsor

    def gen_sponsor_table_2(self, config):
        sponsor = []
        for i in range(0, len(config['logo']), 2):
            sponsor += self.gen_sponsor_table_alt({
                'logo': config['logo'][i:i+2],
                'name': config['name'][i:i+2]
            })
        return sponsor

    def generate_web(self, template, dst):
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
            'normal_sponsor': self.gen_sponsor_table(self.normal_sponsor),
            #'party_sponsor': self.gen_sponsor_table(self.party_sponsor),
            'ryokan': self.md_converter('ryokan')
        }
        with open(dst, 'w') as f:
            f.write(tmpl.render(v))

    def generate_paper(self, templates, dst_dir):
        t = TimeTable(self.timetable_source_file)
        timetable_headings, timetables = t.gen_paper_table()

        r = Room(self.room_source_file)
        room_headings, room_tables = r.gen_room_table()

        v = {
            'cover': {
                # TODO: ここはself.party_sponsorsを入れなくて良いのか？
                'sponsor': self.gen_sponsor_table_2(self.normal_sponsor)
            },
            'timetable': {
                'timetable_headings': timetable_headings,
                'timetables': timetables,
            },
            'room': {

                'room_headings': room_headings,
                'room_tables': room_tables,
            },
            'ryokan': {
                'ryokan': self.md_converter('paper_ryokan')
            },
            'info': {
                'info': self.md_converter('paper_info')
            }
        }
        env = Environment(loader=FileSystemLoader('./', encoding='utf-8'))
        for page_name in list(templates.keys()):
            tmpl = env.get_template(templates[page_name])
            with open(os.path.join(dst_dir, page_name + '.html'), 'w') as f:
                f.write(tmpl.render(v[page_name]))
