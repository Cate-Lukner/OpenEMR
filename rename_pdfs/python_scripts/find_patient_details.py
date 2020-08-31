import sys
import subprocess
import signal
import os
import csv

import re
import pandas as pd
import random


def get_current_patients_df(patient_names_file):
    """
    Extracts the names into a list from the file of patient names.
    """

    df = pd.read_csv(patient_names_file)

    return df 

def find_patient(current_patients_df, txt):

    last_names = current_patients_df['Last'].tolist()

    for i, last in enumerate(last_names):
        with open(txt) as f:
            for line in f:
                match = re.search(r'\b%s\b'%(last.strip().lower()),line.strip().lower())
                if match:
                    # Find the first name and then return the first and last names
                    first = current_patients_df['First'].iloc[i]
                    for line in f:
                        match = re.search(r'\b%s\b'%(first.strip().lower()),line.strip().lower())
                        if match:
                            # Find the first name and then return the first and last names
                            birth = current_patients_df['Birth'].iloc[i]
                            for line in f:
                                match = re.search(r'\b%s\b'%(first.strip().lower()),line.strip().lower())
                                if match:
                                    # Find the first name and then return the first and last names
                                    birth = current_patients_df['Birth'].iloc[i]
                                    return {'last': last, 'first': first, 'birth': birth} 
    else:
        return None

def give_first_and_last():
    # TODO: Add Confirmation of the Patient
    patient_last = input('Type the LAST NAME of the patient: ')
    patient_first = input('Type the FIRST NAME of the patient: ')
    patient_dict = {'last': patient_last, 'first': patient_first, 'birth': None}
    return patient_dict 

def confirm_patient(name_dict):
    if name_dict:
        print(f"The Patient {name_dict['first']} {name_dict['last']} born {name_dict['birth']} was found.")
        confirm = input("Enter (y/n) to confirm the patient: ")
        if confirm[0] == 'y':
            return name_dict
        elif confirm[0] == 'n':
            return give_first_and_last()
        else:
            print("That was not a valid input of (y/n), so we will take that as a no.")
            return give_first_and_last()
    else: 
        return give_first_and_last()

def document_questioning(question):

    question_for_document = input(question)

    if question_for_document:
        return re.sub('/', '-', question_for_document.replace(' ', ''))
    elif (question_for_document == None) or (question_for_document == ' ') or (question_for_document == '\n'):
        return document_questioning("Please type something more.\n")

def main():

    print("\n\n")

    patient_names_file = str(sys.argv[1])
    current_patients_df = get_current_patients_df(patient_names_file)
    
    pdf_name = 'PDFs/' + str(sys.argv[2]) + '.pdf'
    open_pdf = subprocess.Popen("xdg-open '%s'" % pdf_name, shell=True, preexec_fn=os.setpgrp)

    txt_file = 'txt-files/' + sys.argv[2] + '.txt'
    found_patient = find_patient(current_patients_df, txt_file)

    patient_dict = confirm_patient(found_patient)

    date = document_questioning("Please type the date of the document: ") 

    topic = re.sub(' ', '-', document_questioning("What is the document about? "))

    os.killpg(os.getpgid(open_pdf.pid), signal.SIGTERM)

    first = patient_dict["first"]
    last = patient_dict["last"]
    rand_hash = random.getrandbits(30)

    os.rename(pdf_name, f'finished_files/PDFs/{last}_{first}-{topic}-{date}-{rand_hash}.pdf')
    os.rename(txt_file, f'finished_files/TXTs/{last}_{first}-{topic}-{date}-{rand_hash}.txt')

    return patient_dict 
    
if __name__ == "__main__":
    main()
