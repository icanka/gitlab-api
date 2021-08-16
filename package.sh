#!/bin/bash

find_version () {
        version=$(ls --format=single-column "$1" | grep -E -oi '(-[0-9]+-)|([-][0-9a-z]+[.][0-9a-z]*[.]*[0-9a-z]*[.]*[0-9a-z]*((-)|(.tar.gz)|(.zip)|(.tar.bz2)|(.tgz)))' | sed -E 's/-|.tar.gz|.tar.bz2|.zip|.tgz//g')
}


PACKAGE=$1


mkdir $PACKAGE
cd $PACKAGE

#pip download "$PACKAGE" | grep Collecting | cut -d' ' -f2 | grep -Ev "$PACKAGE(~|=|\!|>|<|$)" | grep -oi '^[a-z0-9_.]*[-]*[a-z]*[-]*[a-z]*[-]*' | sed 's/-$//' > package_list.txt
python3.9 -m pip download "$PACKAGE" | grep Collecting | cut -d' ' -f2 | grep -oi '^[a-z0-9_.]*[-]*[a-z]*[-]*[a-z]*[-]*' | sed 's/-$//' > package_list.txt

while read p; do
  pkg_file=$(echo "$p" | sed -E 's/-/_/g')
  file=$(ls --format=single-column | grep -i "^$pkg_file")
  if [[ -z $file ]];then
      file=$(ls --format=single-column | grep -i "^$p")
  fi
  find_version $file
  echo $p==$version >> requirements.txt
done < package_list.txt
rm package_list.txt

