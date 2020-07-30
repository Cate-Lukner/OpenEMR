#!/bin/bash

# Ensure correct directories exist
mkdir -p PDFs/
mkdir -p txt-files/
mkdir -p tiff-files/
mkdir -p finished_files/PDFs
mkdir -p finished_files/TXTs

# Remove spaces from file names
python ./python_scripts/remove-non-alphnum.py

# Get all the PDF files
FILES=( $(find ./PDFs/ -type f -name "*.pdf") )

# Set the current file as file number one
current_file=1

# Loop through all the PDF files
for file in "${FILES[@]}"
do
        # Give the current file and how many files are left.
        printf "\nCurrently on File: $file\n"
        percent=$((100*$current_file/${#FILES[@]}))
        printf "On file $current_file out of ${#FILES[@]} files. $percent%% of the way there.\n"

	# Get the basename of the file
	filename="$(basename "$file" .pdf)"

	# Convert to an image
	magick convert -density 300 "$file" -depth 8 -strip -background white -alpha off ./tiff-files/$filename.tiff
	# Use tesseract to conver to a .txt document
	tesseract ./tiff-files/$filename.tiff ./txt-files/$filename

	# Increment the current file count
	current_files=$((current_file+1))
done

# Clean up the uneeded .tiff files
rm -r ./tiff-files/

# Analyze the documents for patient names and rename accordingly.
for file in $FILES
do
	filename="$(basename "$file" .pdf)"

	python ./python_scripts/mac_find_patient_details.py current_patient_names.csv $filename
done
