import re
import os
import string
import pypi_helper
import time

# test = "soupsieve (<2.0,>1.2) ; python_version < '3.0'"
# test = test.split(" ", 2)[0]
#
packages = ["lxml", "requests"]
# downloaded_package = ["lxml"]
#
# suffix_list = ["]"]
# dist = ["coverage[toml]", "requests"]
# #
# # for item in dist:
# #     for dist in filter(item.endswith, suffix_list):
# #         item = item.split('[')[0]
# #         print(item)
#
#
# def if_empty(item):
#     return True if item == "1.5.7" else False
# text="""
# pytest (>=3.5)
# coverage[toml] (>=5.0.2) ; extra == 'dev'
# hypothesis ; extra == 'dev'
# pytest (>=4.3.0) ; extra == 'dev'
# pycparser
# """
#
# for item in text.strip().split('\n'):
#     print(item)
# splitted = re.split("[\] [/!<>=();']+", DATA4)

# pypi_helper.save_log(packages, "downloaded_FILES", leading_text="URL: ")
# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()