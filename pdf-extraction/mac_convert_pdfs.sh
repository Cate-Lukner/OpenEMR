#!/bin/bash

# Get all the PDF files
FILES=$(find . -type f -name "*.pdf")

# Loop through all the PDF files
for file in $FILES
do
	# Get the basename of the file
	filename=$(basename "$file" .pdf)

	# Convert to an image
	gm convert -density 300 $file -depth 8 -strip -background white -alpha off $filename.tiff
	# Use tesseract to conver to a .txt document
	tesseract $filename.tiff $filename
done


# Clean up the uneeded .tiff files
for file in $FILES
do
	filename=$(basename "$file" .pdf)
	rm $filename.tiff
done
'

