import sys
import subprocess
import signal
import os
import csv

import spacy
import re
import pandas as pd
import random


nlp = spacy.load('en_core_web_sm')

STRIP_TO_NAME = re.compile(r"(patient)?name[:]?", re.IGNORECASE)

def get_current_patients_df(patient_names_file):
    """
    Extracts the names into a list from the file of patient names.
    """

    df = pd.read_csv(patient_names_file)

    return df 

def find_patient(current_patients_df, txt):

    last_names = current_patients_df['Last'].tolist()

    for i, name in enumerate(last_names):
        with open(txt) as f:
            for line in f:
                match = re.search(r'\b%s\b'%(name.strip().lower()),line.strip().lower())
                if match:
                    # Find the first name and then return the first and last names
                    last = name
                    first = current_patients_df['First'].iloc[i]
                    for line in f:
                        match = re.search(r'\b%s\b'%(first.strip().lower()),line.strip().lower())
                        if match:
                            # Find the first name and then return the first and last names
                            birth = print(current_patients_df['Birth'].iloc[i])
                        for line in f:
                            match = re.search(r'\b%s\b'%(first.strip().lower()),line.strip().lower())
                            if match:
                                # Find the first name and then return the first and last names
                                birth = current_patients_df['Birth'].iloc[i]
                                return {'last': last, 'first': first, 'birth': birth} 
    else:
        return None
    

def confirm_patient(name_dict):

    if name_dict:
        print(f"The Patient {name_dict['first']} {name_dict['last']} born {name_dict['birth']} was found.")
        return name_dict
    else: 
        # Need a validation for last, first, and birth
        patient_last = input('No patient was found. Could you please type the last name of the patient? \n')
        patient_first = input('Type the first name of the patient: ')
        patient_birthdate = input('Type the birthdate: ')

        return {'last': patient_last, 'first': patient_first, 'birth': patient_birthdate}

def yes_or_no(question):
    reply = str(input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return 1
    elif reply[0] == 'n':
        return 0
    else:
        return yes_or_no("Please Enter (y/n) ")

def find_date(text_file, patient_dict):
    
    with open(str(text_file), "r") as f:
        content = f.read()
        pattern = r"\d{1,2}[/-]\d{1,2}[/.-]\d{2,4}"
        dates = re.findall(pattern, content)
        if dates != []:
            dates = [date for date in dates if date != patient_dict['birth']]
            dates = list(set(dates))

    for date in dates:
        if (yes_or_no(f'Is "{date}" the date of the document?')):
            doc_date = re.sub(
                '/', '-',
                date 
            )
            return doc_date 
    else: 
        doc_date = input('No date was found. Could you please type the name of the patient? \n')
        doc_date = re.sub(
            '/', '-',
            doc_date 
        )
        return doc_date 

def document_topic(question="What is this document about?\n"):

    document_topic = input(question)

    if document_topic:
        return document_topic
    elif (document_topic == None) or (document_topic == ' ') or (document_topic == '\n'):
        return document_topic("Please type something more.\n")

def main():

    patient_names_file = str(sys.argv[1])
    print("Collecting current patient names..")
    current_patients_df = get_current_patients_df(patient_names_file)
    
    pdf_name = 'PDFs/' + str(sys.argv[2]) + '.pdf'
    print("Opening the pdf..")
    open_pdf = subprocess.Popen("xdg-open '%s'" % pdf_name, shell=True, preexec_fn=os.setpgrp)

    print("Getting the names..")
    txt_file = 'txt-files/' + sys.argv[2] + '.txt'
    patient_dict = find_patient(current_patients_df, txt_file)

    print("Analyzing the names..\n")
    patient_dict = confirm_patient(patient_dict)

    date = find_date(txt_file, patient_dict)

    topic = re.sub(' ', '-', document_topic())

    print("Closing the PDF..")
    os.killpg(os.getpgid(open_pdf.pid), signal.SIGTERM)


    first = patient_dict["first"]
    last = patient_dict["last"]
    rand_hash = random.getrandbits(30)

    os.rename(pdf_name, f'finished_files/PDFs/{last},{first}-{topic}-{date}-{rand_hash}.pdf')
    os.rename(pdf_name, f'finished_files/TXTs/{last},{first}-{topic}-{date}-{rand_hash}.txt')

    return patient_dict 
    
if __name__ == "__main__":
    main()
