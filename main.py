import os
import time
from datetime import datetime
import requests
import parseJson
import pypi_helper
from new_main import extract_urls
from pypi_helper import (
    extract_dependency,
    extract_package_info_dictionary,
    download_file,
)

# from pypi_helper_mock import download_file

# GET /pypi/<project_name>/json
# TODO: check if the file is already downloaded with the same digest.
# TODO: Check if the package names were given correctly.
# TODO: Feature for not downloading extra package dependencies too.
# TODO: Dont create folder if the response is not 200
from progress_bar import printProgressBar

if __name__ == "__main__":
    # print("Please wait while fetching the urls. This may take a while...")
    packages = {"requests"}
    total_url_len = extract_urls(packages, extra_depen=False)
    os.system("cls" if os.name == "nt" else "clear")
    print(len(total_url_len))
    count = 0
    exit(0)
    base_path = "/home/izzetcan/Downloads/linuxPackages/"
    # packages = {'lxml', 'python-active-directory', 'python-gitlab'}

    package_info_list = []
    dependency_set = set()
    downloaded_urls = set()
    failed_urls = set()
    downloaded_packages = set()

    base_url = "https://pypi.org/pypi/package_name/json"
    python_version = "source"  # do NOT download 'source' versions.
    package_type = "bdist_wheel"  # download only bdist_wheel type packages.
    url_log_file = "url_log" + "_" + datetime.today().strftime("%M%H%d%m%y") + ".log"
    request_log_file = (
        "requst_log" + "_" + datetime.today().strftime("%M%H%d%m%y") + ".log"
    )
    log_dir = os.getcwd()

    cwd = os.getcwd()
    # print(cwd)

    copy_packages = packages.copy()
    # print(type(copy_packages))
    while len(copy_packages) > 0:
        # print(copy_packages)
        # print(len(copy_packages))
        for package in copy_packages:
            if package not in downloaded_packages:
                # print("Downloading package " + package)

                packages_directory = os.path.join(base_path, "packages", package)
                if os.path.exists(packages_directory) is False:
                    # print('creating directories: ' + packages_directory + " does not exists")
                    os.makedirs(packages_directory)
                os.chdir(packages_directory)

                url = base_url.replace("package_name", package)
                r = requests.get(url)

                if r.status_code == 200:
                    json_data = r.json()
                    parseJson.save_json(json_data, package)
                    # Get the dependant packages
                    # print(json_data)
                    for dependency in extract_dependency(
                        json_data, base_path, extras=False
                    ):
                        # dependency_set.add(dependency)
                        # print(package + " dependency:  " + "'" + dependency + "'")
                        if dependency not in downloaded_packages:
                            packages.add(dependency)

                    # Get the package dictionary

                    for package_dict in extract_package_info_dictionary(
                        json_data, python_version, package_type
                    ):
                        filename = package_dict["url"].rsplit("/", 1)[1]
                        # print(package_dict['url'])
                        package_info_list.append(package_dict)
                        if package_dict["url"] not in downloaded_urls:
                            # Download the file
                            # print(os.getcwd())
                            # print(package_dict['url'])
                            is_downloaded = download_file(
                                package_dict["url"], package_dict["sha256_digest"]
                            )
                            # Check if it was successfully downloaded
                            if is_downloaded is True:
                                # print(filename + " successfully downloaded.")
                                downloaded_urls.add(package_dict["url"])
                                count += 1
                                # printProgressBar(count, total_url_len, prefix='Progress:', suffix='Complete', length=50)
                                # print(len(downloaded_urls))
                                pypi_helper.log(
                                    "Success: "
                                    + " : "
                                    + package_dict["url"]
                                    + " "
                                    + package_dict["sha256_digest"],
                                    url_log_file,
                                    log_dir,
                                )
                            else:
                                # TODO: Find a better solution to this very quick workaround.
                                # print(filename + " could not be downloaded. Trying again")
                                is_downloaded = download_file(
                                    package_dict["url"], package_dict["sha256_digest"]
                                )
                                if is_downloaded is False:
                                    failed_urls.add(package_dict["url"])
                                    pypi_helper.log(
                                        "Fail: "
                                        + package_dict["url"]
                                        + " "
                                        + package_dict["sha256_digest"],
                                        url_log_file,
                                        log_dir,
                                    )

                else:
                    log_message = (
                        "Could not retrieve api response: Url: "
                        + url
                        + " Status code: "
                        + str(r.status_code)
                    )
                    print(package)
                    print(log_message)
                    pypi_helper.log(log_message, request_log_file, log_dir)
                downloaded_packages.add(package)
                packages.remove(package)
                copy_packages = packages.copy()

    print("Total Successfull Downloads: " + str(len(downloaded_urls)))
    pypi_helper.log(
        "Total Successfull downloads: " + str(len(downloaded_urls)),
        url_log_file,
        log_dir,
    )
    print("Total Successfull Downloads: " + str(len(downloaded_urls)))

    print("Total Failed downloads: " + str(len(failed_urls)))
    pypi_helper.log(
        "Total Failed downloads: " + str(len(failed_urls)), url_log_file, log_dir
    )

    print("Total downloaded packages: " + str(len(downloaded_packages)))
    pypi_helper.log(
        "Total Downloaded packages: " + str(len(downloaded_packages)),
        url_log_file,
        log_dir,
    )
