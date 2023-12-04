# Datos que necesitamos para el web scraping de la URL
# - Categoria
# - Titulo
# - Fecha de publicacion
# - Autor
# - Cuerpo de noticia
# - keywords
# - URL

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# URL principal
url_base = "https://www.elsalvador.com/"

# Configuración de encabezados para solicitudes
headers = {"Accept-Language": "es-SV, es;q=0.5"}

# Obtener la página principal
response = requests.get(url_base, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Extraer categorías principales y secundarias
categorias_principales = [container.find("a").text for container in soup.find_all('li', class_='menu-item menu-item-has-no-children')][:-1]
categorias_secundarias = [container.find("a").text for container in soup.find_all('li', class_='menu-item menu-item-has-children')]

# Construir URLs para scraping
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

# Extraer URLs de noticias
urls = []
categoria_ok = []
for url_categoria in url_ok:
    response = requests.get(url_categoria)
    soup = BeautifulSoup(response.text)
    for container in soup.find_all('div', class_='article-summary'):
        url_noticia = container.h1.a.get('href')
        urls.append(url_noticia)
        categoria_ok.append(url_noticia.split('/')[4])

# Scraping de noticias
data_dict_list = []
for url_noticia in urls:
    try:
        response = requests.get(url_noticia)
        response.raise_for_status()
        soup = BeautifulSoup(response.text)

        # Extracción de datos de la noticia
        title = soup.find('article', class_='detail').h1.text
        summary = soup.find('p', class_='summary').text if soup.find('p', class_='summary') else "No se encontró resumen"
        author = soup.find('p', class_='info-article').a.span.text if soup.find('p', class_='info-article') else "No se encontró autor"
        date = soup.find('span', class_='ago').text if soup.find('span', class_='ago') else "No se encontró fecha"
        full_text = soup.find('div', class_='entry-content').text if soup.find('div', class_='entry-content') else "No se encontró noticia completa"
        keyword_list = [a_tag.text for a_tag in soup.find('div', class_='in-this-article').find_all('a', class_='tag')] if soup.find('div', class_='in-this-article') else ["No se encontraron keywords"]

        # Construir el diccionario
        data_dict = {
            'Titulo': title,
            'Resumen': summary,
            'Autor': author,
            'Fecha': date,
            'Noticia': full_text,
            'Keywords': keyword_list,
            'URL': url_noticia,
        }

        data_dict_list.append(data_dict)

    except requests.exceptions.RequestException as e:
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
        data_dict_list.append(data_dict)

# Crear un DataFrame a partir de la lista de diccionarios
news_elsalvador = pd.DataFrame(data_dict_list)
news_elsalvador['Categoria'] = categoria_ok

# Exportar a CSV los datos recolectados con un timestamp en el nombre del archivo
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
nombre_archivo = f'news_elsalvador_{timestamp}.csv'
news_elsalvador.to_csv(nombre_archivo, index=False)