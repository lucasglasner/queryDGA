## queryDGA

Simple program to download public hydrometeorological data from DGA (Direccion General de Aguas - Ministerio de Obras Publicas - Chile) public server.

The idea is the following:
1)  Enter https://snia.mop.gob.cl/BNAConsultas/reportes
2)  Select variable and a station for download
3)  Solve the captcha manually
4)  Inspect the download button
5)  Go to network options, press the button and then get the cURL (POSIX) request
6)  Go to [https://curlconverter.com/json/](https://curlconverter.com/json/) and transform cURL request to json
7)  Copy json content to DGA_cURL.json file
8)  Check DGA_query.ipynb and DGA_process.ipynb notebooks to learn how to use the package.

---

