#!/bin/bash

PACKAGE=$1
pip download "$PACKAGE" | grep Collecting | cut -d' ' -f2 | grep -Ev "$PACKAGE(~|=|\!|>|<|$)" | grep -oi '^[a-z0-9_.]*[-]*[a-z]*[-]*[a-z]*[-]*' | sed 's/-$//'
# ls --format=single-column | grep -oi '[-][0-9a-z]*[.][0-9a-z]*[.]*[0-9a-z]*-' | sed 's/-//g'
ls --format=single-column | grep -oi '[-][0-9a-z]*[.][0-9a-z]*[.]*[0-9a-z]*[.]*[0-9a-z]*-' | sed 's/-//g'
ls --format=single-column | grep -E -oi '[-][0-9a-z]*[.][0-9a-z]*[.]*[0-9a-z]*[.]*[0-9a-z]*(-)|(.tar.gz)|(.zip)|(.tar.bz2)|(.tgz)' | sed 's/-//g'|wc -l
'[-][0-9a-z]*[.]*[0-9a-z]*[.]*[0-9a-z]*[.]*[0-9a-z]*(-)|(.tar.gz)|(.zip)|(.tar.bz2)|(.tgz)'

ls --format=single-column | grep -E -oi '(-[0-9]+-)|([-][0-9a-z]+[.][0-9a-z]*[.]*[0-9a-z]*[.]*[0-9a-z]*((-)|(.tar.gz)|(.zip)|(.tar.bz2)|(.tgz)))' | sed -E 's/-|.tar.gz|.tar.bz2|.zip|.tgz//g'



#pip download "$PACKAGE" | grep Collecting | cut -d' ' -f2 | grep -Ev "$PACKAGE(~|=|\!|>|<|$)" | sed 's/-$//'