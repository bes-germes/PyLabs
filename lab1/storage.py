import argparse
import json
import os.path


def storage_func(key=None, value=None):
    d = {}

    if not os.path.exists("storage.json"):
        with open("storage.json", "w") as write_file:
            json.dump(d, write_file)
            print("file was made")
            exit(1)

    with open("storage.json", "r+") as write_file:
        try:
            d = json.loads(write_file.read())

        except json.decoder.JSONDecodeError:
            print("File is empty, added syntax")
            json.dump(d, write_file)
            exit(1)

    if key is None:
        return print("enter key plz")
    if value is None:
        with open("storage.json", "r") as write_file:
            result = json.load(write_file)
            if len(result) <= 0:
                return print(None)
            if key in result.keys():
                print(*result[key], sep=", ")
            else:
                return "No such key"
    if key and value:
        if key in d.keys():
            for d_value in d[key]:
                if d_value == value:
                    return print("value is already exist in this key")

            d.setdefault(key, [])
            d[key].append(value)

        else:
            d[key] = [value]

        with open("storage.json", "w") as write_file:
            json.dump(d, write_file)


parser = argparse.ArgumentParser(description="storage script")

parser.add_argument("--key", dest="key_name", type=str)
parser.add_argument("--val", dest="value", type=str)

args = parser.parse_args()

storage_func(args.key_name, args.value)
