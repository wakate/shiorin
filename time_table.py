import csv

from config import Config
from table import Table


class TimeTable(Table):
    def __init__(self, source_path: str, config: Config):
        with open(source_path, newline='') as f:
            self.timetable_sheet = list(csv.reader(f))

    @staticmethod
    def join_cell(source, index):
        dst = []
        if 0 in index:
            for i in index:
                if source[i] != '':
                    dst.append(source[i])
            return '<br>~<br>'.join(dst)
        elif 9 in index:
            if source[6] != '':
                dst.append("<b>%s</b>" % source[12])
                dst.append("[%s]<br>" % source[13])
                dst.append(source[9])
                dst.append("(%s)" % source[11])
            return ' '.join(dst)
        else:
            for i in index:
                if source[i] != '':
                    dst.append(source[i])
            return '/'.join(dst)

    @staticmethod
    def count_session(rows):
        program = list(map(lambda v: v[1], rows))
        find_flag = -1
        flaged_index = -1
        counter = []
        for i, v in enumerate(program):
            counter.append(1)
            if find_flag > 0:
                counter[i] -= 1
                counter[flaged_index] += 1
            try:
                find_index = program.index(v, i + 1)
            except ValueError:
                find_flag = -1
                continue

            if find_index - i > 1:
                find_flag = -1
                continue

            if find_flag < 0:
                find_flag = 1
                flaged_index = i

        return counter

    def gen_rows(self, content):
        # TODO: この設定の仕方やべ〜のでdata/timetable.jsonみたいなのでconfigできるようにする
        table_structure = [
            [0, 1],  # 開始時刻、終了時刻
            [3],  # プログラム（セッション内容）
            [12, 13, 9, 11],  # 詳細 = 発表タイトル [発表区分]\n発表者名（発表者所属）
            [4]  # 座長
        ]
        rows = []
        for row in content:
            tmp = list(map(lambda i: self.join_cell(row, i), table_structure))
            rows.append(tmp)

        return rows

    def gen_tables(self):
        [headings, contents] = self.divide_sheet(self.timetable_sheet)

        tables = []
        for content in contents:
            rows = self.gen_rows(content)
            rows.insert(0, ['時間', 'プログラム', '詳細', '座長'])

            counter = self.count_session(rows)

            table = []
            for i, row in enumerate(rows):
                tmp = []
                for j, cell in enumerate(row):
                    if i == 0:
                        if j == 0:
                            cls = 'time'
                        elif j == 1:
                            cls = 'program'
                        elif j == 2:
                            cls = 'detail'
                        elif j == 3:
                            cls = 'chairperson right_edge'
                        c = '<th class="%s">%s</th>' % (cls, cell)
                    elif j == 2:
                        c = '<td class="detail">%s</td>' % cell
                    elif counter[i] == 0:
                        continue
                    elif j == 0:
                        if counter[i] == 1:
                            c = '<td>%s</td>' % cell
                        else:
                            cc = '%s<br>~<br>%s' % (content[i - 1][0], content[i - 1 + counter[i] - 1][1])
                            c = '<td rowspan="%d">%s</td>' % (counter[i], cc)
                    elif j == 1:
                        if counter[i] == 1:
                            c = '<td>%s</td>' % cell
                        else:
                            c = '<td rowspan="%d">%s</td>' % (counter[i], cell)
                    elif j == 3:
                        if counter[i] == 1:
                            c = '<td class="chairperson right_edge">%s</td>' % cell
                        else:
                            c = '<td class="chairperson right_edge" rowspan="%d">%s</td>' % (counter[i], cell)
                    tmp.append(c)
                table.append(tmp)
            tables.append(table)
        return [headings, tables]

    def gen_paper_table(self):
        headings, contents = self.divide_sheet(self.timetable_sheet)

        sections = []
        for content in contents:
            rows = self.gen_rows(content)
            counter = self.count_session(rows)

            section = []
            for i, row in enumerate(rows):
                tmp = {}
                if counter[i] == 1:
                    tmp['header'] = '%s　　%s' % (row[0].replace('<br>', ' '), row[1])
                    tmp['detail'] = []
                    if row[2] != '':
                        tmp['detail'].append(row[2].replace('<b>', ' '.replace('</b>', ' ')))
                elif counter[i] > 1:
                    tmp['header'] = '%s ~ %s　　%s' % (content[i][0], content[i + counter[i] - 1][1], row[1])
                    d = []
                    for adder in range(counter[i]):
                        d.append(rows[i + adder][2].replace('<b>', ' ').replace('</b>', ' '))
                    tmp['detail'] = d
                else:
                    continue
                section.append(tmp)
            sections.append(section)
        return headings, sections
