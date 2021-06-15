import os
import time

import requests
from pypi_helper import (
    extract_dependency,
    extract_package_info_dictionary,
    download_file,
)
from pypi_helper_mock import download_file

# GET /pypi/<project_name>/json
# TODO: check if the file is already downloaded with the same digest.
# TODO: Check if the package names were given correctly.
# TODO: Feature for not downloading extra package dependencies too.
# TODO: Dont create folder if the response is not 200
if __name__ == "__main__":
    #base_path = os.getcwd()
    base_path = "/home/izzetcan/LinuxExtra/"
    # packages = {'lxml', 'python-active-directory', 'python-gitlab'}
    packages = {"python-gitlab"}

    package_info_list = []
    dependency_set = set()
    downloaded_urls = set()
    failed_urls = set()
    downloaded_packages = set()

    base_url = "https://pypi.org/pypi/package_name/json"
    python_version = "source"
    package_type = "bdist_wheel"

    cwd = os.getcwd()

    # if r.status_code == 200:
    #     json_data = r.json()
    #
    #     python_version = 'source'
    #     package_type = 'bdist_wheel'
    #     for i_json in search_key_recursive_yield(json_data, 'releases'):
    #         for release_version in iterate_value(i_json):
    #             for specific_release in iterate_value(release_version):
    #                 for type in search_key_recursive_yield(specific_release, 'packagetype'):
    #                     for version in search_key_recursive_yield(specific_release, 'python_version'):
    #                         if version['python_version'] != 'source' and type['packagetype'] == 'bdist_wheel':
    #                             #print(version['python_version'] + "  " + type['packagetype'])
    #                             pass
    #                     print(release)

    # extract_package_info_dictionary(json_data,python_version,package_type)

    copy_packages = packages.copy()
    # print(type(copy_packages))
    while len(copy_packages) > 0:
        # print(copy_packages)
        # print(len(copy_packages))
        for package in copy_packages:
            if package not in downloaded_packages:
                print("Downloading package " + package)

                packages_directory = os.path.join(base_path, "packages", package)
                if os.path.exists(packages_directory) is False:
                    os.makedirs(packages_directory)
                os.chdir(packages_directory)

                url = base_url.replace("package_name", package)
                r = requests.get(url)

                if r.status_code == 200:
                    json_data = r.json()

                    # Get the dependant packages
                    for dependency in extract_dependency(json_data,  extras=True):
                        # dependency_set.add(dependency)
                        # print(package + " dependency:  " + "'" + dependency + "'")
                        if dependency not in downloaded_packages: packages.add(dependency)

                    # Get the package dictionary
                    for package_dict in extract_package_info_dictionary(
                        json_data, python_version, package_type
                    ):
                        filename = package_dict["url"].rsplit("/", 1)[1]
                        package_info_list.append(package_dict)
                        if package_dict["url"] not in downloaded_urls:
                            # Download the file
                            is_downloaded = download_file(
                                package_dict["url"], package_dict["sha256_digest"]
                            )
                            # Check if it was successfully downloaded
                            if is_downloaded is True:
                                # print(filename + " successfully downloaded.")
                                downloaded_urls.add(package_dict["url"])
                            else:
                                # TODO: Find a better solution to this very quick workaround.
                                # print(filename + " could not be downloaded. Trying again")
                                is_downloaded = download_file(
                                    package_dict["url"], package_dict["sha256_digest"]
                                )
                                if is_downloaded is False:
                                    failed_urls.add(package_dict["url"])

                else:
                    print(package)
                    print(
                        "Could not retrieve api response: Url: "
                        + url
                        + " Status code: "
                        + str(r.status_code)
                    )
                    print("Request url :")
                downloaded_packages.add(package)
                packages.remove(package)
                copy_packages = packages.copy()

    # print("Total Successfull Downloads: " + str(len(downloaded_urls)))
    # print("Total Failed downloads: " + str(len(failed_urls)))
    # print("Total downloaded packages: " + len(downloaded_packages))
