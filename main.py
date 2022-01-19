import os
from datetime import datetime
from pprint import pprint

import pypi_helper
from new_main import extract_urls_v2
from progress_bar import printProgressBar
from pypi_helper import download_file
from pypi_helper import pip_download_and_return

if __name__ == "__main__":
    package_info_list = set()
    downloaded_urls = set()
    failed_urls = set()
    url_log_file = "url_log" + "_" + datetime.today().strftime("%M%H%d%m%y") + ".log"
    base_path = os.getcwd()
    request_log_file = (
            "requst_log" + "_" + datetime.today().strftime("%M%H%d%m%y") + ".log"
    )
    count = 0

    log_dir = base_path
    cwd = os.getcwd()

    # packages = {"Flask", "SQLAlchemy", "mysqldb-wrapper", "Flask-MySQLdb", "pytest",
    #             "PyGreSQL", "pyquery", "pipenv", "black", "selenium", "Twisted", "bokeh", "fabric2", "Pillow",
    #             "yarn.build", "molecule[docker,lint,ansible]"}
    packages = {"docker", "docker-compose"}

    packages_directory = os.path.join(base_path, "packages")


    # TODO: Muhtemelen url_list icerisinde duplicate itemler var
    for package in packages:
        package_info = pip_download_and_return(package)
        for item in package_info:
            if item: package_info_list.add(tuple(item))
        os.remove(package + '/requirements.txt')

    url_list = extract_urls_v2(package_info_list)
    pprint(len(url_list))

    if os.path.exists(packages_directory) is False:
        os.makedirs(packages_directory)
    os.chdir(packages_directory)

    os.system("cls" if os.name == "nt" else "clear")
    for file in url_list:
        file_name = filename = file["url"].rsplit("/", 1)[1]
        if file["url"] not in downloaded_urls:
            # Download the file
            is_downloaded = download_file(
                file["url"], file["sha256_digest"]
            )
            if is_downloaded is True:
                downloaded_urls.add(file["url"])
                pypi_helper.log(
                    "Success: "
                    + " : "
                    + file["url"]
                    + " "
                    + file["sha256_digest"],
                    url_log_file,
                    log_dir,
                )
                count += 1
            elif is_downloaded is False:
                failed_urls.add(file["url"])
                pypi_helper.log(
                    "Fail: "
                    + file["url"]
                    + " "
                    + file["sha256_digest"],
                    url_log_file,
                    log_dir,
                )
            elif is_downloaded is None:
                pypi_helper.log(
                    "File already exists: "
                    + file["url"]
                    + " "
                    + file["sha256_digest"],
                    url_log_file,
                    log_dir,
                )
                count += 1
        printProgressBar(
            count,
            len(url_list),
            prefix="Progress:",
            suffix="| " + str(count) + " of " + str(len(url_list)) + " |",
            length=50,
        )
