import csv
from jinja2 import Template


class Participant:
    def __init__(self, source_file):
        with open(source_file, newline='') as f:
            self.participant_sheet = list(csv.reader(f))[1:]

        self.index_name = {
            0: 'name',
            1: 'affiliation',
            2: 'sns',
            3: 'role',
            4: 'presentation_type',
            5: 'is_sponsor',
        }
        self.row_looks = {
            'role_simple': Template('{{ role }}'),
            'role_sponsor': Template('{{ is_sponsor }}|{{ role }} ({{ presentation_type }})'),
            'role_speaker': Template('{{ role }} ({{ presentation_type }})'),
            'name': Template('{{ name }}'),
            'detail_simple': Template('{{ affiliation }}'),
            'detail_with_sns': Template('{{ affiliation }}<br>{{ sns }}')
        }
        self.row_tag = [
            # header
            [
                Template('<th class="role">{{ c }}</th>'),
                Template('<th class="name">{{ c }}</th>'),
                Template('<th class="detail right_edge">{{ c }}</th>')
            ],
            # body
            [
                Template('<td class="role">{{ c }}</td>'),
                Template('<td class="name">{{ c }}</td>'),
                Template('<td class="detail right_edge">{{ c }}</td>')
            ]
        ]
        self.sns_service = ['Twitter', 'Facebook', 'Other(GitHub等)']

    def gen_rows(self, contents):
        rows = []
        for row in contents:
            sns = []
            for i, item in enumerate(row[2].replace(' ', '').replace('https://', '**').split('/')):
                if item:
                    sns.append('%s:%s' % (self.sns_service[i], item.replace('**', 'https://')))
            context = {}
            for idx in range(len(row)):
                context[self.index_name[idx]] = row[idx] if idx != 2 else ', '.join(sns)

            tmp = []
            if context['is_sponsor']:
                role = self.row_looks['role_sponsor'].render(context)
            elif context['presentation_type']:
                role = self.row_looks['role_speaker'].render(context)
            elif context['role']:
                role = self.row_looks['role_simple'].render(context)
            else:
                role = ''
            tmp.append(role)
            tmp.append(self.row_looks['name'].render(context))
            if context['sns']:
                detail = self.row_looks['detail_with_sns'].render(context)
            else:
                detail = self.row_looks['detail_simple'].render(context)
            tmp.append(detail)
            rows.append(tmp)
        return rows

    def gen_table(self):
        rows = self.gen_rows(self.participant_sheet)
        table = []
        for row in rows:
            tmp_row = []
            for j, cell in enumerate(row):
                tmp_row.append(self.row_tag[1][j].render(c=cell))
            table.append(tmp_row)

        header = []
        for j, cell in enumerate(['', '氏名', '所属, SNS']):
            header.append(self.row_tag[0][j].render(c=cell))
        table.insert(0, header)

        return table
