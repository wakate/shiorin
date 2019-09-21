import csv
from jinja2 import Template


class Room:
    def __init__(self, source_file):
        with open(source_file, newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            self.room_sheet = list(reader)

        self.row_tag = [
            # header
            [
                Template('<th>{{ c }}</th>'),
                Template('<th class="right_edge">{{ c }}</th>')
            ],
            # body
            [
                Template('<td>{{ c }}</td>'),
                Template('<td class="right_edge">{{ c }}</td>'),
                Template('<td class="left">{{ c }}</td>'),
                Template('<td class="right">{{ c }}</td>')
            ]
        ]

    def divide_sheet(self):
        contents_each_area = []
        heads = []
        for row in self.room_sheet:
            if row[0] == '':
                continue
            elif row[3] in heads:
                contents_each_area[heads.index(row[3])].append(row)
            else:
                heads.append(row[3])
                contents_each_area.append([row])

        return heads, contents_each_area

    def gen_room_table_t(self):
        heads, contents = self.divide_sheet()

        tables = []
        for content in contents:
            room = []
            for i, row in enumerate(content):
                if i == len(content) - 1:
                    room.append(self.row_tag[0][1].render({'c': row[0]}))
                else:
                    room.append(self.row_tag[0][0].render({'c': row[0]}))

            number_of_row = 0
            for row in content:
                if int(row[11]) > number_of_row:
                    number_of_row = int(row[11])

            table = []
            for i in range(4, 4 + number_of_row):
                table_row = []
                for j, row in enumerate(content):
                    if j == len(content) - 1:
                        table_row.append(self.row_tag[1][1].render({'c': row[i]}))
                    else:
                        table_row.append(self.row_tag[1][0].render({'c': row[i]}))
                table.append(table_row)

            table.insert(0, room)
            tables.append(table)

        return heads, tables

    def gen_room_table(self):
        heads, contents = self.divide_sheet()

        tables = []
        for content in contents:
            table = []
            for row in content:
                table_row = [self.row_tag[1][2].render({'c': row[0]})]
                attendances = []
                for i in range(4, 4 + int(row[11])):
                    attendances.append(row[i])
                table_row.append(self.row_tag[1][3].render({'c': ', '.join(attendances)}))
                table.append(table_row)
            tables.append(table)
        return heads, tables
