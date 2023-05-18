import requests

from pypi_helper import (
    extract_package_info_dictionary_v2,
)


def extract_urls_v2(
        package_list
):
    url_list = []
    res = []
    base_url = "https://pypi.org/pypi/package_name/json"

    for package in package_list:
        # package[0] is the package name: ['urllib3', '1.26.6']
        url = base_url.replace("package_name", package[0])
        # Get the JSON response from API for the given package
        r = requests.get(url)
        if r.status_code == 200:
            json_data = r.json()
            # Pass the returned JSON and the desired package version
            for package_dict in extract_package_info_dictionary_v2(json_data, package[1], download_all=False):
                url_list.append(package_dict)
            res = url_list[-40:]
            print(f"last packages 5 element {res}")
    return res
