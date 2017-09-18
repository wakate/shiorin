import csv
from table import Table
from jinja2 import Template
from pprint import pprint


class AbstTable(Table):
    def __init__(self, csv_file):
        self.data_file = csv_file

        self.row_structure = [
            [6],  # 氏名
            [8, 9],  # タイトル, 発表区分
            [10]  # 発表詳細
        ]
        self.index_name = {
            6: 'name',
            8: 'title',
            9: 'type',
            10: 'detail'
        }
        self.row_looks = [
            Template('{{ name }}'),
            Template('{{ title }} [{{ type }}]'),
            Template('{{ detail }}')
        ]
        self.row_tag = [
            # header
            [
                Template('<th class="name">{{ c }}</th>'),
                Template('<th class="title">{{ c }}</th>'),
                Template('<th class="detail right_edge">{{ c }}</th>')
            ],
            # body
            [
                Template('<td class="name">{{ c }}</td>'),
                Template('<td class="title">{{ c }}</td>'),
                Template('<td class="detail right_edge">{{ c }}</td>')
            ]
        ]

    def gen_rows(self, content):
        rows = []
        for row in content:
            tmp = []
            for col, idxs in enumerate(self.row_structure):
                context = {}
                for i in idxs:
                    context[self.index_name[i]] = row[i]
                tmp.append(self.row_looks[col].render(context))
            rows.append(tmp)

        return rows

    def gen_tables(self):
        with open(self.data_file, newline='') as f:
            sheet = list(csv.reader(f))

        [headings, contents] = self.process_sheet(sheet)
        for content in contents:
            pprint(self.gen_rows(content))
