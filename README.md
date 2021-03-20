# web_scrapper

En este proyecto presento un proceso ETL automatizado que tiene como objetivo obtener artículos de varias páginas web, extraer cierta información y transformarla para que se cree un archivo que podra ser cargado a una base de datos. El proceso de cargado no se lo hace puesto que dependera de la base de datos que se use, sin embargo, el archivo final esta creado para subirlo automáticamente a la base.

Este proyecto consta de la siguiente estructura:

* Una carpeta extract que contiene los archivos para hacer la extracción
* Una carpeta transform donde se tiene el archivo para hacer la transformación de la data
* Un archivo pipeline.py que contiene la automatización de los procesos

El objetivo es entender el proceso que un data engineer debe realizar para tener los datos estructurados a fin de que el data scientist este listo para analizarlos 
