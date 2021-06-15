import json


def item_generator(json_input, lookup_key):
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == lookup_key:
                yield v


def item_generator2(json_input, lookup_key):
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == lookup_key:
                yield v
            else:
                yield from item_generator(v, lookup_key)
    elif isinstance(json_input, list):
        for item in json_input:
            yield from item_generator(item, lookup_key)


with open("python-packages.json") as json_file:
    # text_file = open("Output.txt", "w")
    data = json.load(json_file)
    for item in item_generator(data, "query"):
        print(item)
    # for p in data['rows']:
    # print(p['project'])
    # text_file.write(p['project'] + "\n")
    # text_file.close()
