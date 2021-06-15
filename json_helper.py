def search_key_recursive_yield(json_input, search_key):
    if isinstance(json_input, dict):
        for key, value in json_input.items():
            if key == search_key:
                yield {key: value}
            else:
                yield from search_key_recursive_yield(value, search_key)
    elif isinstance(json_input, list):
        for item in json_input:
            yield from search_key_recursive_yield(item, search_key)


def search_key_recursive_return(json_dict, search_key):
    if isinstance(json_dict, dict) and search_key in json_dict:
        return json_dict[search_key]
    elif isinstance(json_dict, list):
        for item in json_dict:
            if isinstance(item, dict):
                found = search_key_recursive_return(item, search_key)
                if found is not None:
                    return found
    elif isinstance(json_dict, dict):
        for key, value in json_dict.items():
            found = search_key_recursive_return(value, search_key)
            if found is not None:
                return found


def get_values(json_data):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            yield value
    elif isinstance(json_data, list):
        yield from get_list_item(json_data)


def get_keys(json_data):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            yield key
    elif isinstance(json_data, list):
        yield from get_list_item(json_data)


def split_dict_items(json_data):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            yield {key: value}
    elif isinstance(json_data, list):
        yield from get_list_item(json_data)


def iterate_value(json_data):
    if isinstance(json_data, dict):
        for value in json_data.values():
            yield from split_dict_items(value)
    elif isinstance(json_data, list):
        yield from get_list_item(list)


def get_list_item(list):
    for item in list:
        yield item


def get_pair(json_dict):
    for key, value in json_dict.items():
        print(key)
        print(value)
        yield {key, value}
