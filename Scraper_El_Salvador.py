# Datos que necesitamos para el web scraping de la URL
# - Categoria
# - Titulo
# - Fecha de publicacion
# - Autor
# - Cuerpo de noticia
# - keywords
# - URL

import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime

url = "https://www.elsalvador.com/"
headers = {"Accept-Language": "es-SV, es;q=0.5"}
results = requests.get(url, headers=headers)

soup = BeautifulSoup(results.text, "html.parser")

# Variables de almacenamiento de datos
categoria_parent = []
categoria = []
titulo = []
fecha = []
autor = []
noticia = []
resumen = []
keywords = []
# ids = []
urls = []
url_ok = []
# img_url = []
data_dict_list = []
categoria_ok = []

# Extraer las categorias dela noticias
categoria_li = soup.find_all('li', class_='menu-item menu-item-has-no-children')
for container in categoria_li:
    categoria.append(container.find("a").text)

categoria_li = soup.find_all('li', class_='menu-item menu-item-has-children')
for container in categoria_li:
    categoria_parent.append(container.find("a").text)

categoria = categoria[:-1]
categoria.remove(categoria[0])

for parent in categoria_parent:
    for cat in categoria:
        url = f'https://www.elsalvador.com/category/{parent.lower().replace(" ", "-")}/{cat.lower().replace(" ", "-")}'
        # print(url)
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Lanza una excepción para errores HTTP (códigos 4xx y 5xx)
            
            if response.status_code == 200:
                # print(f'La página {url} existe.')
                url_ok.append(url)
            else:
                # print(f'La página {url} existe, pero el código de estado es {response.status_code}.')
                continue
        except requests.exceptions.RequestException as e:
            # print(f'Error al intentar acceder a la página {url}: {e}')
            pass

for ur1 in url_ok:
    response = requests.get(ur1)
    soup = BeautifulSoup(response.text)
    
    #Extrae lka noticia de la URL
    url_li = soup.find_all('div', class_='article-summary')
    for container in url_li:
        url0 = container.h1.a.get('href')
        urls.append(url0)
        partes = url0.split('/')
        categoria_ok.append(partes[4])


for ur1 in urls:
    try:
        response = requests.get(ur1)
        response.raise_for_status()
        soup = BeautifulSoup(response.text)
        
        # Título
        titul = soup.find('article', class_='detail')
        title = titul.h1.text
        
        # Resumen
        resumen_tag = soup.find('p', class_='summary')
        summary = resumen_tag.text if resumen_tag else "No se encontró resumen"
        
        # Autor
        auto = soup.find('p', class_='info-article')
        author = auto.a.span.text if auto else "No se encontró autor"
        
        # Fecha
        fecha_li = soup.find('span', class_='ago')
        date = fecha_li.text if fecha_li else "No se encontró fecha"
        
        # Noticia completa
        noticia_full = soup.find('div', class_='entry-content')
        full_text = noticia_full.text if noticia_full else "No se encontró noticia completa"
        
        # Keywords
        keywords_li = soup.find('div', class_='in-this-article')    
        keyword_list = [a_tag.text for a_tag in keywords_li.find_all('a', class_='tag')] if keywords_li else ["No se encontraron keywords"]
        
        # Construir el diccionario
        data_dict = {
            'Titulo': title,
            'Resumen': summary,
            'Autor': author,
            'Fecha': date,
            'Noticia': full_text,
            'Keywords': keyword_list,
            'URL': ur1,
        }
        
        data_dict_list.append(data_dict)

    except requests.exceptions.RequestException as e:
        print(f'Error al intentar acceder a la página {ur1}: {e}')
        data_dict = {
            'Titulo': "Error en la solicitud",
            'Resumen': "Error en la solicitud",
            'Autor': "Error en la solicitud",
            'Fecha': "Error en la solicitud",
            'Noticia': "Error en la solicitud",
            'Keywords': ["Error en la solicitud"],
            'URL': ur1,
        }
        data_dict_list.append(data_dict)

# Crear un DataFrame a partir de la lista de diccionarios
news_elsalvador = pd.DataFrame(data_dict_list)
news_elsalvador['Categoria'] = categoria_ok
# Exportar a CSV los datos recolectados
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
nombre_archivo = f'news_elsalvador_{timestamp}.csv'
news_elsalvador.to_csv(nombre_archivo, index=False)