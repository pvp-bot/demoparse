#!/bin/bash

# run parsedemo.py on all demos in folder
# append resulting csvs together w/ name of folder

dir_name=$(basename $1)

for demo in $1/*.cohdemo
do
	python parsedemo.py "$demo"
done

first="0"


for csv in $1/*.csv
do
	# skip the appended csv if it exists already
	if [ "$csv" == "$1"/"$dir_name".csv ]
	then
		continue
	fi
	# only keep the header on the first file
	if [ "$first" -eq "0" ] 
	then
		head -1 $csv > "$1"/"$dir_name".csv
		first="1"
	fi
	# append all csvs together
	tail -n +2 -q $csv >> "$1"/"$dir_name".csv
done

# upload the appended csv to BQ
python upload_bq.py "$1"/"$dir_name".csv
