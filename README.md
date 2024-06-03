## queryDGA

Simple program to download public hydrometeorological data from DGA (Direccion General de Aguas - Ministerio de Obras Publicas - Chile) public server.

The idea is the following:

1) Enter https://snia.mop.gob.cl/BNAConsultas/reportes
2) Select variable and a station for download
3) Solve the captcha manually
4) Inspect the download button
5) Go to network options, press the button and then get the cURL (POSIX) request
6) Go to [https://curlconverter.com/json/](https://curlconverter.com/json/) and transform cURL request to json
7) Copy json content to DGA_cURL.json file. The file should have something like this in the "data" key:

   ```text
       "filtroscirhform:j_idt100-value": "true",
       "filtroscirhform:j_idt177": "on",
       "filtroscirhform:j_idt102-value": "true",
       "filtroscirhform:fechaDesdeInputDate": "01/01/1990",
       "filtroscirhform:fechaDesdeInputCurrentDate": "05/2024",
       "filtroscirhform:fechaHastaInputDate": "31/01/1992",
       "filtroscirhform:fechaHastaInputCurrentDate": "05/2024",
   ```
8) Check DGA_query.ipynb to learn how to download
9) Check DGA_process.ipynb to postprocess the spreadsheets

---
