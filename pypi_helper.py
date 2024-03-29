import hashlib
import os
import re
from pprint import pprint

import requests
from json_helper import *


def extract_package_info_dictionary(
    json_data, python_version="source", package_type="bdist_wheel"
):
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
                print(version)
                if version == python_version:
                    break

                type = search_key_recursive_return(specific_release, "packagetype")
                if type != package_type:
                    break
                sha256_digest = search_key_recursive_return(specific_release, "sha256")

                # WHAT THE FUCK! spesific_release not release_version
                #url = search_key_recursive_return(release_version, "url")
                url = search_key_recursive_return(specific_release, "url")
                flatten_dict = {
                    "version_number": version_number,
                    "python_version": version,
                    "package_type": type,
                    "sha256_digest": sha256_digest,
                    "url": url,
                }
                print(url)

                yield flatten_dict


# TODO: Do not split required dists with space as sometime the string is like
#  importlib_metadata;python_version<'3.8'
#  zipp;python_version<'3.8'
# coverage[toml]
# requirementslib;
import parseJson


def extract_dependency(
    json_data,
    base_path=None,
    extras=True,
):
    dist_set = set()
    requires_dist = search_key_recursive_return(json_data, "requires_dist")

    if requires_dist is not None:
        for dist in requires_dist:
            if base_path: parseJson.save_text(dist, "requires_dict", path=base_path)

            p = re.compile("[.0-9a-z-]*", re.IGNORECASE)
            m = p.match(dist)

            splitted_dist = re.split("[\][/!<>=(); ']+", dist)
            if extras is False and "extra" in splitted_dist:
                break
            for item in filter(if_empty, splitted_dist.copy()):
                splitted_dist.remove(item)

            dist_set.add(m.group())

            # dist_set.add(m.group())
    else:
        pass

    return dist_set


def download_file(url, sha256_digest=None):
    r = requests.get(url)
    filename = url.rsplit("/", 1)[1]
    # with open(filename, 'wb') as package:
    #   package.write(r.content)
    if os.path.exists(filename):
        return False
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

    # if not filename.endswith('.json'):
    #     filename += '.json'
    # if not text.endswith('\n'):
    #     text += '\n'
    # if path is None:
    #     path = os.getcwd()
    # os.chdir(path)


def save_json_response(json_data):
    package_name = "test"


def if_empty(item):
    return True if item == "" else False


def if_extra(item):
    return True if item == "extra" else False
