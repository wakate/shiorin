import json
import typing


class Config:
    def __init__(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
            self.__load(data)

    @property
    def roomColumnMap(self) -> typing.Dict[str, str]:
        return self.__columnMap["room"]

    @property
    def timetableColumnMap(self) -> typing.Dict[str, str]:
        return self.__columnMap["timetable"]

    def __load(self, data):
        columnMap = data["columnMap"]
        self.__columnMap = {
            "room": columnMap["room"],
            "timetable": columnMap["timetable"],
        }
