# week 4, task 1

import tempfile
import os


class AddException(Exception):
    def __init__(self, class_type):
        self.class_type = str(class_type) + " doesn't exist"


class File:
    def __init__(self, path=""):
        self.path = path
        self.current_position = 0

        if not os.path.exists(self.path):
            open(self.path, 'w').close()

    def __str__(self):
        if self.path:
            return str(self.path)
        else:
            return "file doesn't exist"

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.path, 'r') as f:
            f.seek(self.current_position)

            line = f.readline()
            if not line:
                self.current_position = 0
                raise StopIteration('EOF')

            self.current_position = f.tell()
            return line

    def __add__(self, other_file):
        if other_file:
            if not isinstance(other_file, File):
                raise AddException(File)

        # create new file
        path_to_new_file = os.path.join(tempfile.gettempdir(), "new_file")
        with open(path_to_new_file, "a") as file_add:
            pass

        # write data from the first file to new file
        with open(self.path, "r") as file_self:
            with open(path_to_new_file, "w") as file_add:
                for line in file_self:
                    file_add.write(line)

        # write data from the first file to the end of new file
        with open(other_file.get_path(), "r") as other_file:
            with open(path_to_new_file, "a") as file_add:
                for line in other_file:
                    file_add.write(line)

        return File(path_to_new_file)

    def get_path(self):
        return self.path

    def write(self, data):
        with open(self.path, "w") as file_self:
            file_self.write(data)


path = tempfile.gettempdir()
path_os = os.path.join(tempfile.gettempdir())


path_1 = os.path.join("text_1.txt")
path_2 = os.path.join("text_2.txt")

file_one = File(path_1)

for line in file_one:
    print(line)

file_two = File(path_2)

try:
    file = file_one + file_two
except AddException as ae:
    print(ae.class_type)



