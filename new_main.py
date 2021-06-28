import requests
from pypi_helper import (
    extract_dependency,
    extract_package_info_dictionary,
)

# GET /pypi/<project_name>/json
# TODO: check if the file is already downloaded with the same digest.
# TODO: Check if the package names were given correctly.
# TODO: Feature for not downloading extra package dependencies too.
# TODO: Dont create folder if the response is not 200
def extract_urls(packages, extra_depen=False):
    #packages = {"python-active-directory"}
    url_set = set()
    package_list = set()

    base_url = "https://pypi.org/pypi/package_name/json"
    python_version = "source"  # do NOT download 'source' versions.
    package_type = "bdist_wheel"  # download only bdist_wheel type packages.

    copy_packages = packages.copy()
    while len(copy_packages) > 0:
        for package in copy_packages:
            if package not in package_list:

                url = base_url.replace("package_name", package)
                r = requests.get(url)

                if r.status_code == 200:
                    json_data = r.json()

                    for dependency in extract_dependency(
                            json_data, extras=extra_depen
                    ):
                        if dependency not in package_list:
                            packages.add(dependency)

                    # Get the package dictionary
                    for package_dict in extract_package_info_dictionary(
                            json_data, python_version, package_type
                    ):
                        if package_dict["url"] not in url_set:
                            url_set.add(package_dict["url"])

                else:
                    # log_message = (
                    #         "Could not retrieve api response: Url: "
                    #         + url
                    #         + " Status code: "
                    #         + str(r.status_code)
                    # )
                    return r.raise_for_status()

                package_list.add(package)
                packages.remove(package)
                copy_packages = packages.copy()
    return url_set
