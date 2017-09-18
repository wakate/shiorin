class Table:
    @staticmethod
    def process_sheet(sheet):
        headings = []
        sep = []
        for i, row in enumerate(sheet):
            if row[0] == '開始時刻':
                sep.append(i)
            elif row[0] != '' and row[3] == '':
                headings.append(row[0])
        contents = []
        for i, v in enumerate(sep):
            if i + 1 < len(sep):
                contents.append(sheet[v + 1:sep[i + 1] - 1])
            else:
                contents.append(sheet[v + 1:])

        return [headings, contents]