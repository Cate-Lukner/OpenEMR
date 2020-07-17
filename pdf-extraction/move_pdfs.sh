#!/bin/bash

# Get all the PDF files
FILES=$(find . -type f -name "*.txt")

# Loop through all the PDF files
for file in $FILES
do
	# Get the basename of the file
	filename=$(basename "$file" .txt)

    PATIENT=$(python find_patient_details.py $filename.txt $filename.pdf)

    echo $PATIENT
done


# Clean up the uneeded .txt files
for file in $FILES
do
    rm $file
done

