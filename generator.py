import csv
from jinja2 import Environment, FileSystemLoader


def join(source, index):
    dst = []
    for i in index:
        if source[i] != '':
            dst.append(source[i])
    return '/'.join(dst)


def count_into_session(reader):
    # session index is 2
    counter = {}
    for row in reader:
        if row[2] in counter:
            counter[row[2]] += 1
        else:
            counter[row[2]] = 1
    return counter


def gen_table(filename):
    ## セッション内容が同一なら同じセッションとして扱う
    ## 開始時刻, 終了時刻, セッション内容, 座長, 発表カテゴリ, 発表者名, 発表者所属, 発表タイトル, 発表区分
    with open(filename, newline='') as f:
        table = [
            [2],  # プログラム（セッション内容）
            [0, 1],  # 開始時刻、終了時刻
            [7, 8, 5, 6],  # 詳細 = 発表タイトル（発表区分）、発表者名（発表者所属）
            [3]  # 座長
        ]

        env = Environment(loader=FileSystemLoader('./', encoding='utf-8'))
        tmpl = env.get_template('template.html')
        # tmpl.render(name='Hoge')

        header = next(csv.reader(f))
        content = list(csv.reader(f))
        counter = count_into_session(content)

        tbl = [['プログラム', '時間', '詳細', '座長']]
        for row in content:
            tmp = list(map(lambda i: join(row, i), table))
            tbl.append(tmp)

        program = list(map(lambda v: v[0], tbl))
        find_flag = -1
        flaged_index = -1
        count_list = []
        for i, v in enumerate(program):
            count_list.append(1)
            if find_flag > 0:
                count_list[i] -= 1
                count_list[flaged_index] += 1
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

        tbl2 = []
        for i, row in enumerate(tbl):
            tmp = []
            for j, cell in enumerate(row):
                if j == 0 or j == 3:
                    if count_list[i] == 0:
                        continue
                    elif count_list[i] == 1:
                        tmp.append("<td>%s</td>" % cell)
                    else:
                        tmp.append("<td rowspan=\"%d\">%s</td>" % (count_list[i], cell))
                else:
                    tmp.append("<td>%s</td>" % cell)
            tbl2.append(''.join(tmp))
            tmp = []

        v = {
            'table': tbl2,
        }
        html = tmpl.render(v)
        f = open('hoge.html', 'w')
        f.write(html)
        f.close()


gen_table('sample.csv')
