import os
import sys
import glob
import re
import string

pth = "./PDFs/"
dir_show = os.listdir(pth)
allow = string.ascii_letters + string.digits + "-" + "_"

# initializing bad_chars_list
remove_special_chars = [';', ':', '!', "*", '>', '^', '<']

for list_file in dir_show:
    if list_file.endswith(".pdf"):
        fileNamePrefix = list_file[:-4]
        filteredFileNamePrefix = re.sub('[^%s]' % allow, '_', fileNamePrefix)
        #filteredFileNamePrefix = filter(lambda i: i not in remove_special_chars, filteredFileNamePrefix)
        path = os.path.join(pth, list_file)
        newname=os.path.join(pth, filteredFileNamePrefix+".pdf")
        # print(newname)
        os.rename(path,newname)
