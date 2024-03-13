## queryDGA

Simple program to download public hydrometeorological data from DGA (Direccion General de Aguas - Ministerio de Obras Publicas - Chile) public server.

The idea is the following:
1)  Enter https://snia.mop.gob.cl/BNAConsultas/reportes
2)  Select variable and a station for download
3)  Solve the captcha manually
4)  Inspect the download button
5)  Go to network options, press the button and then get the cURL (POSIX) request
6)  Copy-paste to DGA_cURL textfile of this repository
7)  Use dga_request.py utility program for massive download

---

### dga_request.py

This script can be run in two ways: 
1) Edit the last chunk of the script and run from the shell or your favorite GUI:
```python
if __name__ == '__main__':
    path_DGA_curl = 'DGA_cURL'
    DGA_curl = open(path_DGA_curl).read() # <--- Open cURL string
    response, _ = dga_download_request(dga_curl=DGA_curl,
                                       fileprefix='RioLigua',
                                       output_dir='.',      
                                       startyear=2000,
                                       endyear=2015)
```
```bash
$ python3 dga_request.py
```

2) Import the functions and use them directly on your own routines:
```python
import sys
pathtothisrepository='/blabla/blabla/'
sys.path.append(pathtothisrepository)
from dga_request import *


path_DGA_curl = f'{pathtothisrepository}/DGA_cURL'
DGA_curl = open(path_DGA_curl).read() # <--- Open cURL string
response, _ = dga_download_request(dga_curl=DGA_curl,
                                   fileprefix='RioLigua',
                                   output_dir='.',      
                                   startyear=2000,
                                   endyear=2015)
```

This should download one excel spreadsheet per year of available data, in case there is no data for the requested year the spreadsheet is considered corrupt and deleted. It is suggested to check the downloaded years and run the script again if any year was not downloaded correctly. 

---

### dga_request.py

This script is used to postprocess all the excel spreadsheets and export the 
timeseries to a single .csv file with all the aviable data.
Work in progress.
