import hashlib
import re

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
                if version == python_version:
                    break
                type = search_key_recursive_return(specific_release, "packagetype")
                if type != package_type:
                    break
                sha256_digest = search_key_recursive_return(specific_release, "sha256")
                url = search_key_recursive_return(release_version, "url")
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
def extract_dependency(json_data, extras=True):
    suffix_list = ["]"]
    dist_set = set()
    requires_dist = search_key_recursive_return(json_data, "requires_dist")

    if requires_dist is not None:
        for dist in requires_dist:
            splitted_dist = re.split("[\][/!<>=(); ']+", dist)
            if extras is False and "extra" in splitted_dist:
                break
            for item in filter(if_empty, splitted_dist.copy()):
                splitted_dist.remove(item)
            # print(splitted_dist)
            # dist_list = [x.strip() for x in dist.split(';')]
            # if len(dist_list) > 2: print(dist_list)
            # dist = dist_list[0].split(' ')[0].strip()
            # if the dependency is given as extra. Ex: 'coverage[toml]'
            # for char in filter(dist.endswith, suffix_list): dist = dist.split('[')[0]
            dist_set.add(splitted_dist[0])

    return dist_set


def download_file(url, sha256_digest=None):
    r = requests.get(url)
    filename = url.rsplit("/", 1)[1]
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


def if_empty(item):
    return True if item == "" else False


def if_extra(item):
    return True if item == "extra" else False
