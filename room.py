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
            Template('<th class="">{{ c }}</th>'),
            # body
            Template('<td class="">{{ c }}</td>'),
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

    def gen_room_table(self):
        contents = self.divide_sheet()

        tables = []
        for head, content in contents.items():
            rooms = list(map(lambda r: self.row_tag[0].render({'c': r[0]}), content))

            number_of_row = 0
            for row in content:
                if int(row[11]) > number_of_row:
                    number_of_row = int(row[11])

            table = []
            for i in range(4, 4 + number_of_row):
                table_row = []
                for row in content:
                    table_row.append(self.row_tag[1].render({'c': row[i]}))
                table.append(table_row)

            table.insert(0, rooms)
            tables.append(table)

        return list(contents.keys()), tables
