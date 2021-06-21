import json
import os


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


def save_json(json_data, filename, mode='w', path=None):
    if not filename.endswith('.json'):
        filename += '.json'
    if path is None:
        path = os.getcwd()
    os.chdir(path)
    with open(filename, mode) as json_file:
        json.dump(json_data, json_file)

def save_text(text, filename, path=None):
    if not text.endswith('\n'):
        text += '\n'
    if path is None:
        path = os.getcwd()
    os.chdir(path)
    with open(filename, 'a') as text_file:
        text_file.write(text)

