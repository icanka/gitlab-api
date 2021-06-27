import re
from pprint import pprint

p = re.compile("[0-9a-z-]*", re.IGNORECASE)
with open("requires_dict.json", "r") as file:
    lines = file.readlines()
    for line in lines:
        print(p.match(line.strip()))
        m = p.match(line.strip())
        print(type(m.group()))
