# task 1, week 3

import sys


class FileReader:
    def __init__(self, path_to_file):
        self.path = path_to_file

    def read(self):
        try:
            with open(self.path, "r") as file:
                str = ""
                for line in file:
                    str += line
                return str
        except FileNotFoundError:
            return ""


if __name__ == "__main__":
    file = sys.argv[1]
    reader = FileReader(file)
    print(reader.read())
