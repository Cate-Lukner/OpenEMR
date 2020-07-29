# OpenEMR

## Getting Started

**Dependencies:**

Python 3.8.3  
Tesseract 4.1.1  
ImageMagick 6.9.11-22  
Pandas 1.0.5

Ensure dependencies are installed: 
```bash
brew install python # Fedora: dnf install python
brew install tesseract # Fedora: dnf install tesseract
brew install imagemagick # Fedora: dnf install imagemagick
pip install pandas # Fedora: sudo python -m pip install pandas
```

## Key Files and Directories

*Important*: Create the file named exactly as `current_patient_names.csv` formated as follows:  
```
Last,First,Birth
Smith,John,07/04/1776
Washington,George,02/22/1732
```
*Notice the commands, last-first-birth format, no spaces, and no extra line at the end.*  

Place all PDFs to be converted and renamed in `PDFs`. If the directory does not exist, create it using the following command (or your GUI):
```bash
mkdir PDFs
```

All renamed PDFs will be placed in `finished_files/PDFs`. All renamed Text documents will be placed in `finished_files/TXTs`. 
  
## Key Commands 

Ensure the files have the necessary permissions by running:
```bash
chmod + x *.sh
```

To convert all the PDFs into txt documents and rename them, run:
```bash
./mac_convert_and_rename.sh # Linux: ./convert_and_rename.sh
```

If all the PDFs and txt documents have already been converted, you can run:
```bash
./mac_rename.sh # Linux: ./rename.sh
```
You can "pause" the renaming process with `CTRL+C` and resume using the command above. 
  
  
