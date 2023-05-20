#!/bin/bash

source_folder="."
destination_folder="/home/klyx/Sync/skole/p4/prosjekt/data_drone_2"

if [ -d "$destination_folder" ]; then
	folder_number=1
	while true; do
		new_folder_name="$(basename "$destination_folder")_$folder_number"
		new_folder_path="$destination_folder/$new_folder_name"
		if [ ! -d "$new_folder_path" ]; then
			break
		fi
		((folder_number++))
	done

	mkdir "$new_folder_path"
	cp "$source_folder"/*.csv "$new_folder_path"
	cd $new_folder_path
	python3 ../plot_5.py
	echo "Files committed to $new_folder_path"
	xdg-open plot_tid.png
else
	echo "Destination folder does not exist."
fi

