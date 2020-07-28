# OpenEMR

## Getting Started

**Dependencies:**

Python 3.8.3  
Tesseract 4.1.1  
ImageMagick 6.9.11-22  
Pandas 1.0.5

Ensure dependencies are installed: 
```
brew install python # Fedora: dnf install python
brew install tesseract # Fedora: dnf install tesseract
brew install imagemagick # Fedora: dnf install imagemagick
pip install pandas # Fedora: sudo python -m pip install pandas
```

## Key Commands 

Ensure the files have the necessary permissions by running:
```
chmod + x *.sh
```

To convert all the PDFs into txt documents and rename them, run:
```
./mac_convert_and_rename.sh # Linux: ./convert_and_rename.sh
```

If all the PDFs and txt documents have already been converted, you can run:
```
./mac_rename_files.sh # Linux: ./rename_files.sh
```
  
All renamed PDFs will be placed in `finished_files/PDFs`. All renamed Text documents will be placed in `finished_files/TXTs`. 
  
  