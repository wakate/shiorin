import csv
from table import Table


class TimeTable(Table):
    def __init__(self, csv_file):
        self.data_file = csv_file

    @staticmethod
    def join_cell(source, index):
        dst = []
        if 0 in index:
            for i in index:
                if source[i] != '':
                    dst.append(source[i])
            return '<br>~</br>'.join(dst)
        elif 6 in index:
            if source[6] != '':
                dst.append("<b>%s</b>" % source[8])
                dst.append("[%s]<br>" % source[9])
                dst.append(source[6])
                dst.append("(%s)" % source[7])
            return ' '.join(dst)
        else:
            for i in index:
                if source[i] != '':
                    dst.append(source[i])
            return '/'.join(dst)

    @staticmethod
    def count_session(cells):
        program = list(map(lambda v: v[1], cells))
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
        table_structure = [
            [0, 1],  # 開始時刻、終了時刻
            [3],  # プログラム（セッション内容）
            [8, 9, 6, 7],  # 詳細 = 発表タイトル [発表区分]\n発表者名（発表者所属）
            [4]  # 座長
        ]
        rows = []
        for row in content:
            tmp = list(map(lambda i: self.join_cell(row, i), table_structure))
            rows.append(tmp)

        return rows

    def gen_timetables(self):
        with open(self.data_file, newline='') as f:
            sheet = list(csv.reader(f))

        [headings, contents] = self.process_sheet(sheet)

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
