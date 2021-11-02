import hashlib
import os
import re
import subprocess
from pathlib import Path

import parseJson
import requests
from json_helper import *


def extract_package_info_dictionary(json_data, pkg_version, python_version, package_type, package_name):
    for i_json in search_key_recursive_yield(json_data, "releases"):
        count = 0

        for release_version in iterate_value(i_json):
            flatten_dict = {}
            version_number = list(release_version)[0]
            # Unpack each releases' value
            for specific_release in iterate_value(release_version):
                version = search_key_recursive_return(
                    specific_release, "python_version"
                )

                # Commented out; only check package type dont check python_version.
                # if version in python_version:
                #     break

                type = search_key_recursive_return(specific_release, "packagetype")

                # if type in package_type:

                sha256_digest = search_key_recursive_return(specific_release, "sha256")

                url = search_key_recursive_return(specific_release, "url")
                flatten_dict = {
                    "version_number": version_number,
                    "python_version": version,
                    "package_type": type,
                    "sha256_digest": sha256_digest,
                    "url": url,
                }

                yield flatten_dict


# TODO: Do not split required dists with space as sometime the string is like
#  importlib_metadata;python_version<'3.8'
#  zipp;python_version<'3.8'
# coverage[toml]
# requirementslib;


def extract_dependency(
        json_data,
        package_name=None,
        base_path=None,
        extras=True,

):
    dist_set = set()
    # for i_json in search_key_recursive_yield(json_data, "releases"):
    #     for release_version in iterate_value(i_json):
    #         for k in release_version.keys():
    #             print(package_name)
    #             package = package_name + "==" + k
    #             package = {package}
    #             print(package)
    #             for dependency in extract_dependency_pip(package):
    #                 dist_set.add(dependency)
    # print(dist_set)

    requires_dist = search_key_recursive_return(json_data, "requires_dist")

    if requires_dist is not None:
        for dist in requires_dist:
            if base_path:
                parseJson.save_text(dist, "requires_dict", path=base_path)
        for dist in requires_dist:
            p = re.compile("[.0-9a-z-]*", re.IGNORECASE)
            m = p.match(dist)

            splitted_dist = re.split("[\][/!<>=(); ']+", dist)
            # print(splitted_dist)
            if extras is False and "extra" in splitted_dist:
                break
            for item in filter(if_empty, splitted_dist.copy()):
                splitted_dist.remove(item)

            dist_set.add(m.group())
    else:
        pass

    return dist_set


def extract_dependency_pip(package):
    package_set = set()

    for item in package:
        old_cwd = os.getcwd()
        os.chdir('./pip-package')
        packages = subprocess.run(["./pip.sh", item], capture_output=True)
        packages = packages.stdout
        packages = packages.decode("utf-8")
        os.chdir(old_cwd)

        for package in packages.split():
            package_set.add(package)

    return package_set


def download_file(url, sha256_digest=None):
    filename = url.rsplit("/", 1)[1]
    if os.path.exists(filename):
        # print("File exists.")
        if sha256_digest is not None:
            # print("Calculating digest for file for comparision.")
            calculated_digest = calculate_sha256_digest(filename)
            return None if calculated_digest == sha256_digest else False
        return None
    r = requests.get(url)
    open(filename, "wb").write(r.content)
    if sha256_digest is not None:
        calculated_digest = calculate_sha256_digest(filename)
        return True if calculated_digest == sha256_digest else False
    return True


def calculate_sha256_digest(filename):
    sha256_digest = hashlib.sha256()
    with open(filename, "rb") as file:
        # Read and update hash string value in block of 4K
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_digest.update(byte_block)
    return sha256_digest.hexdigest()


def dump_finish_log(iterable, filename, leading_text=None):
    # timestamp format: xxyyzzjjyy minute, hour, day, month, year
    file = open(filename, "a")
    if not type(iterable) is str:
        for item in iterable:
            if not item.endswith("\n"):
                item += "\n"
            if leading_text:
                file.write(leading_text)
            file.write(item)
    file.close()


def log(log_text, log_file, log_dir):
    log_file = os.path.join(log_dir, log_file)
    with open(log_file, "a") as file:
        if not log_text.endswith("\n"):
            log_text += "\n"
        file.write(log_text)


def save_json_response(json_data):
    package_name = "test"


def if_empty(item):
    return True if item == "" else False


def if_extra(item):
    return True if item == "extra" else False


def pip_download_and_return(package_name):
    package_list = []
    data_folder = Path(package_name)
    file_to_open = data_folder / "requirements.txt"
    return_code = subprocess.run(["./package.sh", package_name], timeout=180).returncode
    file = open(file_to_open, "r")
    lines = file.readlines()
    for line in lines:
        package_and_version = line.split('==')
        # strip newline from version string
        package_and_version[1] = package_and_version[1].strip('\n')
        package_list.append(package_and_version)
    return package_list


# Iterate through versions on the returned JSON response. Return the matching ones.
def extract_package_info_dictionary_v2(json_data, package_version):
    for i_json in search_key_recursive_yield(json_data, "releases"):
        for release_version in iterate_value(i_json):
            flatten_dict = {}
            version_number = list(release_version)[0]
            # We found our desired version
            if version_number == package_version:
                for specific_release in iterate_value(release_version):
                    version = search_key_recursive_return(specific_release, "python_version")
                    type = search_key_recursive_return(specific_release, "packagetype")
                    sha256_digest = search_key_recursive_return(specific_release, "sha256")
                    url = search_key_recursive_return(specific_release, "url")
                    flatten_dict = {
                        "version_number": version_number,
                        "python_version": version,
                        "package_type": type,
                        "sha256_digest": sha256_digest,
                        "url": url,
                    }
                    yield flatten_dict
