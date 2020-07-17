import sys
import subprocess
import signal
import os

import spacy
import re
from datefinder import find_dates

nlp = spacy.load('en_core_web_sm')

REMOVE_NAME = re.compile(r"(patient)?name[:]?", re.IGNORECASE)

def yes_or_no(question):
    reply = str(input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return 1
    elif reply[0] == 'n':
        return 0
    else:
        return yes_or_no("Please Enter (y/n) ")

def get_names(doc):
    names = []
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            names.append(ent.text)

    if names != []:
        names = list(set(names))
    
    return names 

def find_correct_name(names_list):
    for name in names_list:
        if (yes_or_no(f'Is "{name}" the patient?')):
            patient = re.sub(
                REMOVE_NAME, '', 
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
        pattern = r"\d{2}[/-]\d{2}[/.-]\d{4}"
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

def main():
    
    pdf_name = str(sys.argv[2])
    print("Opening the pdf..")
    open_pdf = subprocess.Popen("xdg-open '%s'" % pdf_name, shell=True, preexec_fn=os.setpgrp)

    file_name = str(sys.argv[1])
    file_text = open(file_name).read()

    print("Analyzing the ents..")
    file_doc = nlp(file_text)

    print("Getting the names..")
    names_list = get_names(file_doc)

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
