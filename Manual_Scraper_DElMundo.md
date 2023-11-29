# Scraper_D_El_Mundo.py

Este código es un script en Python que realiza web scraping para recopilar noticias del sitio web "[diario.elmundo.sv](https://diario.elmundo.sv/)". A continuación, te proporciono una explicación detallada del código:


### Importación de bibliotecas

```py
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import re` 
```
-   `requests`: Realiza solicitudes HTTP.
-   `datetime`: Obtiene la fecha y hora actual.
-   `BeautifulSoup`: Analiza el HTML de las páginas web.
-   `pandas`: Trabaja con DataFrames.
-   `re`: Realiza operaciones de expresiones regulares.

### Obtener la página principal

```py
url = "https://diario.elmundo.sv/"
headers = {"Accept-Language": "es-SV, es;q=0.5"}
response = requests.get(url, headers=headers)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")` 
```
Se hace una solicitud HTTP a la página principal del diario "El Mundo" y se crea un objeto `BeautifulSoup` para analizar el contenido HTML de la página.

### Recopilar categorías y URLs

```py
categorias = soup.find_all(class_='d-block')
categoria_ok = [re.sub(r"\s+", "", categoria.text) for categoria in categorias]
url_cat = [categoria.get('href', '') for categoria in categorias]` 
```
Se extraen las categorías y las URLs de las secciones de noticias del sitio.

### Eliminar elementos no deseados

```py
categorias_no_deseadas = {"Más", ""}
categoria_ok = [categoria for categoria in categoria_ok if categoria not in categorias_no_deseadas]
url_cat = [url for url in url_cat if url]

if len(categoria_ok) >= 1 and len(url_cat) >= 1:
    del categoria_ok[:1]
    del url_cat[:1]
else:
    print("Las listas no tienen suficientes elementos para eliminar.")` 
```
Se eliminan categorías no deseadas y se asegura de que las listas tengan al menos dos elementos.

### Recopilar URLs de noticias y sus categorías

```py
urls = []
categoria = []
for ur1 in url_cat:
    response = requests.get(ur1)
    soup = BeautifulSoup(response.text)

    url_li = soup.find_all('div', class_='col-md-8 article-image') + soup.find_all('div', class_='col-md-4 article-item')
    for container in url_li:
        url0 = container.a.get('href')
        urls.append(url0)
        partes = url0.split('/')
        categoria.append(partes[3])` 
```
Se obtienen URLs de noticias y sus categorías asociadas.

### Recopilar datos de noticias

```py
news_data = []
for url in urls:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text)

    titul = soup.find('h1', class_='title-article')
    title = titul.text

    resumen_tag = soup.find('div', class_='article-subTitle')
    summary = re.sub(r"\s+", "", resumen_tag.text) if resumen_tag else "No se encontró resumen"

    auto = soup.find('span', class_='article-byline')
    author = auto.text.strip() if auto else "No se encontró autor"

    fecha_li = soup.find('time', class_='publishing-date')
    date = fecha_li.text.strip() if fecha_li else "No se encontró fecha"

    noticia_full = soup.find('div', class_='article-body')
    full_text = noticia_full.text.strip() if noticia_full else "No se encontró noticia completa"

    # keyword_list = [a_tag.text for a_tag in soup.find('div', class_='_magnetEntConent_443-1').find_all('a', class_='_magnetEntNameent_443-1')] if soup.find('div', class_='_magnetEntConent_443-1') else ["No se encontraron keywords"]

    data_dict = {
        'Titulo': title,
        'Resumen': summary,
        'Autor': author,
        'Fecha': date,
        'Noticia': full_text,
        'URL': url,
    }
    news_data.append(data_dict)` 
```
Se extraen datos de las noticias, como título, resumen, autor, fecha y contenido.

### Crear un DataFrame y exportar a CSV

```py
news_df = pd.DataFrame(news_data)
news_df['Categoria'] = categoria

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
filename = f"news_delmundo_test_{timestamp}.csv"
news_df.to_csv(filename, index=False)` 
```
Se crea un DataFrame con la información recopilada y se exporta a un archivo CSV con un nombre que incluye la marca de tiempo.