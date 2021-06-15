import re
import os
import string

test = "soupsieve (<2.0,>1.2) ; python_version < '3.0'"
test = test.split(" ", 2)[0]

packages = ["lxml", "requests"]
downloaded_package = ["lxml"]

suffix_list = ["]"]
dist = ["coverage[toml]", "requests"]
#
# for item in dist:
#     for dist in filter(item.endswith, suffix_list):
#         item = item.split('[')[0]
#         print(item)


def if_empty(item):
    return True if item == "1.5.7" else False


DATA = "Hey, you-/what] are you doing here!?"
DATA2 = "idna (>=2.0.0) ; extra == 'secure'"
DATA2 = "idna>=2.0.0 ; extra == 'secure'"
DATA4 = "PySocks[toml] (!=1.5.7,<2.0,>=1.5.6) ; extra == ''''''socks'"
splitted = re.split("[\] [/!<>=();']+", DATA4)
print(splitted)
list = filter(if_empty, splitted)

for item in list:
    print(item)

# Prints ['Hey', 'you', 'what', 'are', 'you', 'doing', 'here']
