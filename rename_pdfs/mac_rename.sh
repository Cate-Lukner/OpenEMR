# Get all the PDF files
FILES=$(find ./ -type f -name "*.pdf")

for file in $FILES
do
	filename="$(basename "$file" .pdf)"

	python ./python_scripts/mac_find_patient_details.py current_patient_names.csv $filename
done
