import csv


class Room:
    def __init__(self, csv_filename):
        self.room_csv = csv_filename

    def divide_sheet(self):
        with open(self.room_csv, newline='') as f:
            sheet = list(csv.reader(f))
