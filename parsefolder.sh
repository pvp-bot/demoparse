#!/bin/bash

# run parsedemo.py on all demos in folder
# append resulting csvs together w/ name of folder

SKIPPARSE=false
SKIPUPLOAD=false

while getopts 'i:su' flag; do
        case "${flag}" in
                i) INPUT=${OPTARG} ;;
                s) SKIPPARSE=true ;;
				u) SKIPUPLOAD=true ;;
        esac
done



dir_name=$(basename $INPUT)

if [ "$SKIPPARSE" = false ]; then
	for demo in $INPUT/*.cohdemo
	do
		python parsedemo.py "$demo"
	done
fi

first=true


for csv in $INPUT/*.csv
do
	# skip the appended csv if it exists already
	if [ "$csv" == "$INPUT"/"$dir_name".csv ]
	then
		continue
	fi
	# only keep the header on the first file
	if [ "$first" = true ] 
	then
		head -1 $csv > "$INPUT"/"$dir_name".csv
		first=false
	fi
	# append all csvs together
	tail -n +2 -q $csv >> "$INPUT"/"$dir_name".csv
done

# upload the appended csv to BQ
if [ "$SKIPUPLOAD" = false ]; then
	python upload_bq.py "$INPUT"/"$dir_name".csv
fi
