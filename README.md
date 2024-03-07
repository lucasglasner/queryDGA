### queryDGA

Simple program to download public hydrometeorological data from DGA (Direccion General de Aguas - Ministerio de Obras Publicas - Chile) public server.

The idea is the following:
1)  Enter https://snia.mop.gob.cl/BNAConsultas/reportes
2)  Select data for download
3)  Solve the captcha
4)  Download the time series of interest on a short period
5)  Inspect the download and get the cURL (POSIX) request
6)  Copy-paste to DGA_cURL textfile of this repository
7)  Edit dga_request.py with outputfile names and years
8)  Run dga_request.py

