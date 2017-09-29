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
                Template('<td class="right_edge">{{ c }}</td>')
            ]
        ]

    def divide_sheet(self):
        contents_each_area = {}
        for row in self.room_sheet:
            if row[0] == '':
                continue
            elif row[3] in contents_each_area:
                contents_each_area[row[3]].append(row)
            else:
                contents_each_area[row[3]] = [row]

        return contents_each_area

    def gen_room_table_t(self):
        contents = self.divide_sheet()

        tables = []
        for head, content in contents.items():
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

        return list(contents.keys()), tables

    def gen_room_table(self):
        contents = self.divide_sheet()

        tables = []
        for head, content in contents.items():
            table = []
            for row in content:
                table_row = [self.row_tag[1][0].render({'c': row[0]})]
                attendances = []
                for i in range(4, 4 + int(row[11])):
                    attendances.append(row[i])
                table_row.append(self.row_tag[1][0].render({'c': ', '.join(attendances)}))
                table.append(table_row)
            tables.append(table)
        return list(contents.keys()), tables
