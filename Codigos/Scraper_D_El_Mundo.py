import requests
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import re

# Obtener la página principal
url = "https://diario.elmundo.sv/"
headers = {"Accept-Language": "es-SV, es;q=0.5"}
response = requests.get(url, headers=headers)
response.raise_for_status()

# Crear objeto BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Recopilar categorías y URLs
categorias = soup.find_all(class_='d-block')
categoria_ok = [re.sub(r"\s+", "", categoria.text) for categoria in categorias]
url_cat = [categoria.get('href', '') for categoria in categorias]

# Eliminar elementos no deseados
categorias_no_deseadas = {"Más", ""}
categoria_ok = [categoria for categoria in categoria_ok if categoria not in categorias_no_deseadas]
url_cat = [url for url in url_cat if url]

# Asegurarse de que haya al menos dos elementos en las listas
if len(categoria_ok) >= 1 and len(url_cat) >= 1:
    # Eliminar los primeros dos elementos
    del categoria_ok[:1]
    del url_cat[:1]
else:
    print("Las listas no tienen suficientes elementos para eliminar.")

# Recopilar URLs de noticias y sus categorías
urls = []
categoria = []
for ur1 in url_cat:
    response = requests.get(ur1)
    soup = BeautifulSoup(response.text)

    # Extraer noticias de la URL
    url_li = soup.find_all('div', class_='col-md-8 article-image') + soup.find_all('div', class_='col-md-4 article-item')
    for container in url_li:
        url0 = container.a.get('href')
        urls.append(url0)
        partes = url0.split('/')
        categoria.append(partes[3])

# Recopilar datos de noticias
news_data = []
for url in urls:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text)

    # Extraer datos de la noticia
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

    # Construir el diccionario
    data_dict = {
        'Titulo': title,
        'Resumen': summary,
        'Autor': author,
        'Fecha': date,
        'Noticia': full_text,
        # 'Keywords': keyword_list,
        'URL': url,
    }
    news_data.append(data_dict)

# Crear un DataFrame a partir de la lista de diccionarios
news_df = pd.DataFrame(news_data)
news_df['Categoria'] = categoria

# Exportar los datos recopilados a un archivo CSV
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
filename = f"news_delmundo_test_{timestamp}.csv"
news_df.to_csv(filename, index=False)