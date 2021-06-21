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
text="""
pytest (>=3.5)
coverage[toml] (>=5.0.2) ; extra == 'dev'
hypothesis ; extra == 'dev'
pytest (>=4.3.0) ; extra == 'dev'
pycparser
"""

for item in text.strip().split('\n'):
    print(item)
#splitted = re.split("[\] [/!<>=();']+", DATA4)

