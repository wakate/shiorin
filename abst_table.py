import csv
from table import Table
from jinja2 import Template


class AbstTable(Table):
    def __init__(self, source_file):
        with open(source_file, newline='') as f:
            self.timetable_sheet = list(csv.reader(f))

        self.row_structure = [
            [9],  # 氏名
            [12, 13],  # タイトル, 発表区分
            [14]  # 発表詳細
        ]
        self.index_name = {
            9: 'name',
            12: 'title',
            13: 'type',
            14: 'detail'
        }
        self.row_looks = [
            Template('{{ name }}'),
            Template('{{ title }}<br>[{{ type }}]'),
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
            if row[self.row_structure[0][0]] == '':
                continue
            tmp = []
            for col, idxs in enumerate(self.row_structure):
                context = {}
                for i in idxs:
                    context[self.index_name[i]] = row[i]
                tmp.append(self.row_looks[col].render(context))
            rows.append(tmp)

        return rows

    def gen_tables(self):
        [headings, contents] = self.divide_sheet(self.timetable_sheet)

        tables = []
        for content in contents:
            rows = self.gen_rows(content)
            rows.insert(0, ['氏名', 'タイトル', '概要'])
            table = []
            for i, row in enumerate(rows):
                tmp_row = []
                for j, cell in enumerate(row):
                    if i <= 1:
                        tmp_row.append(self.row_tag[i][j].render(c=cell))
                    else:
                        tmp_row.append(self.row_tag[1][j].render(c=cell))
                table.append(tmp_row)
            tables.append(table)

        return [headings, tables]
