#!/bin/bash

# When the end of the collection is reached and there are no additional records to retrieve,
# the Link header is absent and the resulting array is empty.

curl -i -k --request GET --header \
"PRIVATE-TOKEN: SxeBz8HLcrDKqxXKsdjN" \
"https://gitlab/api/v4/projects?pagination=keyset&per_page=1&order_by=id"


# send parameter as payload
# curl --request POST --header "Content-Type: application/json" \
# --data '{"name":"<example-name>", "description":"<example-description"}' "https://gitlab/api/v4/projects"

# Or send them as query string
# curl --request POST "https://gitlab/api/v4/projects?name=<example-name>&description=<example-description>"
