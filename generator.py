import csv
from jinja2 import Environment, FileSystemLoader


def join_cell(source, index):
    dst = []
    if 0 in index:
        for i in index:
            if source[i] != '':
                dst.append(source[i])
        return '<br>~</br>'.join(dst)
    elif 5 in index:
        # [7, 8, 5, 6],  # 詳細 = 発表タイトル [発表区分]\n発表者名（発表者所属）
        if source[5] != '':
            dst.append("<b>%s</b>" % source[7])
            dst.append("[%s]<br>" % source[8])
            dst.append(source[5])
            dst.append("(%s)" % source[6])
        return ' '.join(dst)
    else:
        for i in index:
            if source[i] != '':
                dst.append(source[i])
        return '/'.join(dst)


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


def gen_table(filename):
    with open(filename, newline='') as f:
        table_structure = [
            [0, 1],  # 開始時刻、終了時刻
            [2],  # プログラム（セッション内容）
            [7, 8, 5, 6],  # 詳細 = 発表タイトル [発表区分]\n発表者名（発表者所属）
            [3]  # 座長
        ]

        env = Environment(loader=FileSystemLoader('./', encoding='utf-8'))
        tmpl = env.get_template('template.html')

        sheet = list(csv.reader(f))
        titles = []
        sep = []
        for i, row in enumerate(sheet):
            if row[0] == '開始時刻':
                sep.append(i)
            elif row[0] != '' and row[1] == '':
                titles.append(row[0])
        contents = []
        for i, v in enumerate(sep):
            if i + 1 < len(sep):
                contents.append(sheet[v + 1:sep[i + 1] - 1])
            else:
                contents.append(sheet[v + 1:])

        tables = []
        for content in contents:
            cells = [['時間', 'プログラム', '詳細', '座長']]
            for row in content:
                tmp = list(map(lambda i: join_cell(row, i), table_structure))
                cells.append(tmp)

            counter = count_session(cells)

            table = []
            for i, row in enumerate(cells):
                tmp = []
                for j, cell in enumerate(row):
                    if i == 0:
                        c = '<th class="right">%s</th>' % cell if j == 3 else '<th>%s</th>' % cell
                    elif j == 2:
                        c = '<td>%s</td>' % cell
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
                            c = '<td class="right">%s</td>' % cell
                        else:
                            c = '<td class="right" rowspan="%d">%s</td>' % (counter[i], cell)
                    tmp.append(c)
                table.append(tmp)
            tables.append(table)

        v = {
            'tables': tables,
            'titles': titles
        }
        html = tmpl.render(v)
        f = open('hoge.html', 'w')
        f.write(html)
        f.close()


gen_table('sample.csv')
