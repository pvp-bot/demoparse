#!/bin/bash

# run the parseholder script on on all subfolders in a folder
# each subfolder being a collection of demos from a single scrim

dir_name=$(basename $1)

for dir in $1/*
do
	if [ -d "$dir" ]; then
		sh parsefolder.sh $dir
	fi
done