import csv
from jinja2 import Environment, FileSystemLoader


def join(source, index):
    dst = []
    for i in index:
        if source[i] != '':
            dst.append(source[i])
    return ', '.join(dst)


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

        reader = csv.reader(f)
        header = next(reader)
        content = list(reader)
        # counter = count_into_session(content)
        tbl = []
        tbl.append('<tr>')
        for cell in ['プログラム', '時間', '詳細', '座長']:
            tbl.append('<th>')
            tbl.append(cell)
            tbl.append('</th>')
        tbl.append('</tr>')

        for row in content:
            tbl.append('<tr>')
            for index in table:
                cell = join(row, index)
                # if cell in counter:
                tbl.append('<td>')
                tbl.append(cell)
                tbl.append('</td>')
            tbl.append('</tr>')

        v = {
            'table': ''.join(tbl)
        }
        html = tmpl.render(v)
        print(html)


gen_table('sample.csv')
