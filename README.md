## queryDGA

Simple program to download public hydrometeorological data from DGA (Direccion General de Aguas - Ministerio de Obras Publicas - Chile) public server.

The idea is the following:

1) Enter https://snia.mop.gob.cl/BNAConsultas/reportes
2) Select variable and a region
3) Solve the captcha manually
   ![alt](static/DGA_captcha.png)
4) Select a station to download and select a random time range (just a month is enough)
5) Inspect the download button (before using it)
6) Go to network options, press the button and then get the cURL (POSIX) request
   ![alt](static/DGA_cURL.png)
7) Go to [https://curlconverter.com/json/](https://curlconverter.com/json/) and transform cURL request to json
8) Copy json content to DGA_cURL.json file. The file should have something like this in the "data" key:

   ```text
           "filtroscirhform": "filtroscirhform",
           "filtroscirhform:regionFieldSetId-value": "true",
           "filtroscirhform:j_idt30-value": "filtroscirhform:j_idt45",
           "filtroscirhform:j_idt59": "on",
           "filtroscirhform:panelFiltroEstaciones-value": "true",
           "filtroscirhform:region": "5",  <------------------------ USER SELECTED REGION IN THE WEBPAGE (NOT LOOPABLE)
           "filtroscirhform:selectBusqForEstacion": "1",
           "filtroscirhform:cuenca": "-1",
           "filtroscirhform:estacion": "",
           "g-recaptcha-response": "",
           "filtroscirhform:j_idt100-value": "true",
           "filtroscirhform:j_idt181": "on",           <------------------------ STATION ID (LOOPABLE)
           "filtroscirhform:j_idt102-value": "true",
           "filtroscirhform:fechaDesdeInputDate": "01/01/1990",     <------------------------ START DATE (LOOPABLE)
           "filtroscirhform:fechaDesdeInputCurrentDate": "01/2011", 
           "filtroscirhform:fechaHastaInputDate": "31/12/2010",
           "filtroscirhform:fechaHastaInputCurrentDate": "12/2011",     <------------------------ END DATE (LOOPABLE)
           "filtroscirhform:generarxls": "Generar XLS",
           "javax.faces.ViewState": "-1017629065942579622:-7489475727910640494"
   ```
9)  example.ipynb to learn how to download and postprocess DGA spreadsheets

---

### Dependencies

* requests
* numpy
* pandas
* openpyxl
* tqdm
* json
