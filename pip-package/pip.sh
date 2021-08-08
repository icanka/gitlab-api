#!/bin/bash

PACKAGE=$1
pip download "$PACKAGE" | grep Collecting | cut -d' ' -f2 | grep -Ev "$PACKAGE(~|=|\!|>|<|$)" | grep -oi '^[a-z0-9_.]*[-]*[a-z]*[-]*[a-z]*[-]*' | sed 's/-$//'