# Data-Science

# Desarrollo de un Sistema de Análisis de Noticias Salvadoreñas

## Objetivo General

El objetivo principal de este proyecto es aplicar los fundamentos de ciencia de datos para desarrollar un sistema integral de análisis de noticias salvadoreñas. Se abordarán diferentes etapas, desde la obtención de datos mediante web scraping hasta la implementación de modelos de aprendizaje automático y procesamiento del lenguaje natural, culminando con la creación de una interfaz interactiva utilizando Streamlit.

## Tareas Específicas

### Recolección de Datos

Se utilizaron técnicas de web scraping o APIs para obtener noticias de un periódico salvadoreño, por ejemplo, El Diario de Hoy.

### Secuencia de Pasos en el Web Scraping

1. **Análisis del Código de la Página Principal:** Identificación del menú.
2. **Extracción de Categorías:** Obtención de las categorías principales de noticias a partir del menú.
3. **Obtención de Subcategorías:** Identificación de las subcategorías asociadas a cada categoría principal.
4. **Análisis de URLs:** Determinación de las combinaciones existentes de categorías y subcategorías.
5. **Web Scraping de Categorías:** Obtención de las URLs individuales de cada noticia.
6. **Exploración de URLs de Noticias:** Extracción de información detallada, como título, resumen, fecha de publicación, autor, cuerpo de la noticia, palabras clave y URL.
7. **Almacenamiento de Datos:** Guardado de cada conjunto de datos en una lista individual.
8. **Conversión a Diccionario:** Transformación de las listas en un diccionario.
9. **Transformación a DataFrame:** Conversión del diccionario en un DataFrame de pandas para análisis posterior.
10. **Exportación del DataFrame:** Guardado como archivo CSV agregando un timestamp para individualizar cada extracción de datos.
