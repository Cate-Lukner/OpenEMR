import sys
import subprocess
import signal
import os
import csv

import spacy
import re


nlp = spacy.load('en_core_web_sm')

STRIP_TO_NAME = re.compile(r"(patient)?name[:]?", re.IGNORECASE)

def get_current_patients(patient_names_file):
    """
    Extracts the names into a list from the file of patient names.
    Could potentially change this to read CSV files. 
    """

    # TODO: Read specific columns from CSV into arrays or dicts

    with open(patient_names_file) as f:
        patient_names = f.readlines()
    patient_names = [x.strip().lower() for x in patient_names]

    return patient_names 

def yes_or_no(question):
    reply = str(input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return 1
    elif reply[0] == 'n':
        return 0
    else:
        return yes_or_no("Please Enter (y/n) ")

def get_names(doc, current_patients, txt):
    found_names = []

    """
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            found_names.append(str(ent.text).strip().lower())
    
    # Have it compare against current patient names

    if found_names != []:
        possible_names = []
        for name in found_names:
            for patient in current_patients:
                if patient in name:
                    possible_names.append(name)
        possible_names = list(set(possible_names))

    if possible_names == []:
        print("this ran")
        # Have it compare against current patient names
        with open(txt) as f:
            for line in f:
                for patient in current_patients:
                    if patient in str(line).strip().lower():
                        possible_names.append(line)
    """

    for name in current_patients:
        with open(txt) as f:
            for line in f:
                match = re.search(r'\b%s\b'%(name),line.strip().lower())
                if match:
                    # Find the first name and then return the first and last names
                    found_names.append(name)
    
    return found_names 

def find_correct_name(names_list):

    # TODO: Check if name was found (rather than iterating). If not, prompt user to type the name. 

    for name in names_list:
        if (yes_or_no(f'Is "{name}" the patient?')):
            patient = re.sub(
                STRIP_TO_NAME, '', 
                str(name).lower().strip()
            )
            patient = re.sub(
                ' ', '-',
                patient.strip()
            )
            print(f'Great! {patient} is the patient')
            return patient
    else: 
        patient_name = input('No name was found. Could you please type the name of the patient? \n')
        patient = re.sub(
            ' ', '-',
            patient_name.strip().lower()
        )
        return patient

def find_birthdate(text_file):
    
    with open(str(text_file), "r") as f:
        content = f.read()
        pattern = r"\d{1,2}[/-]\d{1,2}[/.-]\d{2,4}"
        dates = re.findall(pattern, content)
        if dates != []:
            dates = list(set(dates))

    for date in dates:
        if (yes_or_no(f'Is "{date}" the birthdate?')):
            birthdate = re.sub(
                '/', '-',
                date 
            )
            print(f'Great! The {birthdate} is correct')
            return birthdate 
    else: 
        birthdate = input('No date was found. Could you please type the name of the patient? \n')
        birthdate = re.sub(
            '/', '-',
            birthdate
        )
        return birthdate

# TODO: Create a function that asks the user what is the document about

def main():

    patient_names_file = str(sys.argv[1])
    print("Collecting current patient names..")
    current_patients = get_current_patients(patient_names_file)
    
    pdf_name = str(sys.argv[3])
    print("Opening the pdf..")
    open_pdf = subprocess.Popen("xdg-open '%s'" % pdf_name, shell=True, preexec_fn=os.setpgrp)

    file_name = str(sys.argv[2])
    file_text = open(file_name).read()

    print("Analyzing the ents..")
    file_doc = nlp(file_text)

    print("Getting the names..")
    names_list = get_names(file_doc, current_patients, sys.argv[2])

    print("Analyzing the names..\n")
    name = find_correct_name(names_list)

    print("\nFinding the birthdates..\n")
    birthdate = find_birthdate(file_name)

    print("Closing the PDF..")
    os.killpg(os.getpgid(open_pdf.pid), signal.SIGTERM)

    name_and_birthdate = str(name) + '-' + str(birthdate)
    print(name_and_birthdate)

    return name_and_birthdate 
    
if __name__ == "__main__":
    main()
