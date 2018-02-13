import argparse
import tempfile
import json
import os


def add_note(data, input_key, input_value):
    if key in data:
        if key == input_key:
            values = data.get(key)
            values.append(input_value)
            data.update({key: values})
            print(data)
            return data

    values = [str(value)]
    data[input_key] = values
    print(data)
    return data


def write_to_storage(storage_path, key, value):
    path_to_file_storage = os.path.join(tempfile.gettempdir(), "storage.data")
    if not os.path.exists(path_to_file_storage):
        with open(path_to_file_storage, "w", encoding='utf-8') as file:
            print('Creating file "storage.data"...')

    with open(path_to_file_storage, "r+", encoding='utf-8') as file:
        first_string = file.readline()
        if first_string is '':
            print('File "storage.data" is empty.')
            print("Loading data...")
            data = {}
            data = add_note(data, key, value)
            json.dump(data, file, indent=4, ensure_ascii=False)
            print("Done.")
        else:
            file.seek(0)
            data = json.load(file, encoding='utf-8')
            data = add_note(data, key, value)
            file.seek(0)
            json.dump(data, file, indent=4, ensure_ascii=False)


def get_value(storage_path, input_key):
    path_to_file_storage = os.path.join(tempfile.gettempdir(), "storage.data")
    if not os.path.exists(path_to_file_storage):
        print('File "storage.data" doesn\'t exist.')
        return None
    else:
        with open(path_to_file_storage, "r+", encoding='utf-8') as file:
            data = json.load(file, encoding='utf-8')
            keys = list(data.keys())
            for key in keys:
                if key == input_key:
                    return data.get(key)

            return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--key", help="keys")
    parser.add_argument("-v", "--value", help="values")
    key = parser.parse_args().key
    value = parser.parse_args().value

    path = os.path.join(tempfile.gettempdir())

    if key and value:
        print("key:", key)
        print("values:", value)
        write_to_storage(path, key, value)
    elif key and not value:
        values = get_value(path, key)
        if values:
            values = list(values)
            for i in range(len(values)):
                print(values[i], end='')
                if i is not len(values) - 1:
                    print(", ", end='')
        else:
            print(None)
    else:
        print(None)
