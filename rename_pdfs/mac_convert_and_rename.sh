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
FILES=$(find . -type f -name "*.pdf")

# Loop through all the PDF files
for file in $FILES
do
	# Get the basename of the file
	filename="$(basename "$file" .pdf)"

	# Convert to an image
	magick convert -density 300 "$file" -depth 8 -strip -background white -alpha off ./tiff-files/$filename.tiff
	# Use tesseract to conver to a .txt document
	tesseract ./tiff-files/$filename.tiff ./txt-files/$filename
done

# Clean up the uneeded .tiff files
rm -r ./tiff-files/

# Analyze the documents for patient names and rename accordingly.
for file in $FILES
do
	filename="$(basename "$file" .pdf)"

	python ./python_scripts/mac_find_patient_details.py current_patient_names.csv $filename
done
