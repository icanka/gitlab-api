import pprint

import requests

pp = pprint.PrettyPrinter(indent=4)


def walk(node):
    for key, item in node.items():
        if isinstance(item, dict):
            walk(item)
        else:
            pp.pprint(f"{key}: {item}")


def print_key_is_dict(dictionary):
    list = []
    for key, item in dictionary.items():
        if isinstance(item, dict):
            list.append(key)
    return list


def search_key(key_name, dictionary):
    for key, item in dictionary.items():
        if key == key_name:
            pp.pprint(f"{key}: {item}")
            return
    print(
        f"No such key found. Try searching in these keys:",
        print_key_is_dict(dictionary),
    )

    # if isinstance(item, dict):
    #     depth = + 1
    #     search_key(key_name, item)


def print_keys(node):
    for key, item in node.items():
        print(type(key))


params = {}
response = requests.get(
    f"https://jenkins.local:8090/api/v4/projects/8",
    verify=False,
    headers={"PRIVATE-TOKEN": "Y75WeQJrqNB7tSSUzvQ3"},
)

data = response.json()
pp.pprint(type(data))

dates_pattern = r"^(?P<year>d{4})-(?P<month>d{2})-(?P<day>d{2})"

for project in data:
    search_key("kind", project)
    # print(project['name'])

if response:
    print("Request is successful.")
else:
    print("Request returned an error.")
    print(response.text)
