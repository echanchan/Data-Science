# Scraper_El_Salvador.py

Este código es un script en Python que realiza web scraping para recopilar noticias del sitio web "[www.elsalvador.com](https://www.elsalvador.com/)". A continuación, te proporciono una explicación detallada del código:

### Importación de bibliotecas
```py
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime` 
```
-   `requests`: Se utiliza para realizar solicitudes HTTP a la web.
-   `BeautifulSoup`: Sirve para analizar el HTML de las páginas web y extraer información.
-   `pandas`: Se usa para trabajar con estructuras de datos tabulares (DataFrames).
-   `datetime`: Utilizado para obtener la fecha y hora actual.

### Configuración de variables

```py
url_base = "https://www.elsalvador.com/"
headers = {"Accept-Language": "es-SV, es;q=0.5"}` 
```
-   `url_base`: La URL principal del sitio web que se va a escrapear.
-   `headers`: Encabezados de la solicitud HTTP, en este caso, se especifica el idioma.

### Obtención de la página principal

```py
response = requests.get(url_base, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")` 
```
Se realiza una solicitud HTTP a la página principal y se crea un objeto `BeautifulSoup` para analizar el contenido HTML de la página.

### Extracción de categorías principales y secundarias


```py
categorias_principales = [container.find("a").text for container in soup.find_all('li', class_='menu-item menu-item-has-no-children')][:-1]
categorias_secundarias = [container.find("a").text for container in soup.find_all('li', class_='menu-item menu-item-has-children')]` 
```
Se extraen las categorías principales y secundarias del menú del sitio web.

### Construcción de URLs para scraping

```py
url_ok = []
for parent in categorias_secundarias:
    for cat in categorias_principales:
        url = f'https://www.elsalvador.com/category/{parent.lower().replace(" ", "-")}/{cat.lower().replace(" ", "-")}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            if response.status_code == 200:
                url_ok.append(url)
        except requests.exceptions.RequestException as e:
            pass
```
Se construyen las URLs para realizar el scraping, combinando las categorías principales y secundarias.

### Extracción de URLs de noticias


```py
urls = []
categoria_ok = []
for url_categoria in url_ok:
    response = requests.get(url_categoria)
    soup = BeautifulSoup(response.text)
    for container in soup.find_all('div', class_='article-summary'):
        url_noticia = container.h1.a.get('href')
        urls.append(url_noticia)
        categoria_ok.append(url_noticia.split('/')[4])
```
Se extraen las URLs de noticias de las páginas correspondientes a cada categoría.

### Scraping de noticias


```py
data_dict_list = []
for url_noticia in urls:
    try:
        response = requests.get(url_noticia)
        response.raise_for_status()
        soup = BeautifulSoup(response.text)

        # Extracción de datos de la noticia

        # ... (se omite la extracción de información para mantener la explicación concisa)

        data_dict_list.append(data_dict)

    except requests.exceptions.RequestException as e:
        # Manejo de errores en caso de problemas al acceder a la página
        print(f'Error al intentar acceder a la página {url_noticia}: {e}')
        # En caso de error, agregar datos de error al diccionario
        data_dict = {
            'Titulo': "Error en la solicitud",
            'Resumen': "Error en la solicitud",
            'Autor': "Error en la solicitud",
            'Fecha': "Error en la solicitud",
            'Noticia': "Error en la solicitud",
            'Keywords': ["Error en la solicitud"],
            'URL': url_noticia,
        }
        data_dict_list.append(data_dict)` 
```
Se realiza el scraping de cada noticia, extrayendo información como título, resumen, autor, fecha, contenido, palabras clave, etc.

### Creación de un DataFrame y exportación a CSV

```py
news_elsalvador = pd.DataFrame(data_dict_list)
news_elsalvador['Categoria'] = categoria_ok

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
nombre_archivo = f'news_elsalvador_{timestamp}.csv'
news_elsalvador.to_csv(nombre_archivo, index=False)` 
```
Se crea un DataFrame de pandas a partir de la lista de diccionarios `data_dict_list` que contiene la información de las noticias. Se añade la columna `Categoria` y luego se exportan los datos a un archivo CSV con un nombre que incluye la marca de tiempo.