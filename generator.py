import csv
from jinja2 import Environment, FileSystemLoader


def join(source, index):
    dst = []
    if 0 in index:
        for i in index:
            if source[i] != '':
                dst.append(source[i])
        return '<br>~</br>'.join(dst)
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
            [7, 8, 5, 6],  # 詳細 = 発表タイトル（発表区分）、発表者名（発表者所属）
            [3]  # 座長
        ]

        env = Environment(loader=FileSystemLoader('./', encoding='utf-8'))
        tmpl = env.get_template('template.html')

        next(csv.reader(f))
        content = list(csv.reader(f))

        cells = [['時間', 'プログラム', '詳細', '座長']]
        for row in content:
            tmp = list(map(lambda i: join(row, i), table_structure))
            cells.append(tmp)

        counter = count_session(cells)

        table = []
        for i, row in enumerate(cells):
            tmp = []
            for j, cell in enumerate(row):
                if i == 0:
                    tmp.append("<th>%s</th>" % cell)
                elif j == 0:
                    if counter[i] == 0:
                        continue
                    elif counter[i] == 1:
                        tmp.append("<td>%s</td>" % cell)
                    else:
                        c = "%s<br>~<br>%s" % (content[i - 1][0], content[i - 1 + counter[i] - 1][1])
                        tmp.append("<td rowspan=\"%d\">%s</td>" % (counter[i], c))
                elif j == 1 or j == 3:
                    if counter[i] == 0:
                        continue
                    elif counter[i] == 1:
                        tmp.append("<td>%s</td>" % cell)
                    else:
                        tmp.append("<td rowspan=\"%d\">%s</td>" % (counter[i], cell))
                else:
                    tmp.append("<td>%s</td>" % cell)
            table.append(tmp)

        v = {
            'table': table,
        }
        html = tmpl.render(v)
        f = open('hoge.html', 'w')
        f.write(html)
        f.close()


gen_table('sample.csv')
