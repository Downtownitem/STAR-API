from typing import List
import requests
from bs4 import BeautifulSoup
import os
from pdfminer.high_level import extract_text

URL = 'https://standards.nasa.gov/all-standards?page=0'
URL2 = 'https://standards.nasa.gov/all-standards?page=1'
STANDAR_NAME = 'standar_links.txt'
PDF_LINKS = 'pdf_links.txt'

URL3 = 'https://www.nasa.gov/nesc/knowledge-products/nesc-technical-bulletins/'


def get_links(url: str) -> list:
    names = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find(class_='usa-table cols-7')
        lister = table.find_all('a')
        for anchor in lister:
            names.append(anchor.get_text())
        return names[3:]
    else:
        print('404')
    return None


def get_pdf2(url: str) -> list:
    names = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        lister = soup.find_all('a')
        for anchor in lister:
            link = anchor.get('href')
            if str(link).endswith('.pdf'):
                names.append(link)
        return names
    else:
        print('404')


def scrap_text(self):
    try:
        response = requests.get(self.url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        soup = soup.find("section", {"id": "content"})
        for script in soup(["script", "style"]):  # remove all javascript and stylesheet code
            script.extract()
        text = " ".join(t.strip() for t in soup.stripped_strings)

        return text
    except requests.RequestException as e:
        return f"An error occurred while fetching the page: {e}"


def create_links(file_name: str) -> None:
    sufix_names = get_links(URL) + get_links(URL2)
    complete_links = []
    sufix_text = 'https://standards.nasa.gov/standard/NASA/'
    with open(file_name, 'w') as f:
        for element in sufix_names:
            if element == 'NASA-HDBK-1004':
                element = 'NASA-HDBK-1004-0'
            element = element.replace(".", "")
            element = element.replace("  ", "-")
            element = element.replace(" ", "-")

            f.write(sufix_text + element + '\n')
            complete_links.append(sufix_text + element)
    return complete_links


def create_file_pdfs_2(file_name: str) -> None:
    sufix_names = get_pdf2(URL3)
    complete_links = []
    with open(file_name, 'w') as f:
        for element in sufix_names:
            element = element.replace('\u202f', '?')
            f.write(element + '\n')
            complete_links.append(element)
        # Cuarto link de recursos
        f.write('https://www.nasa.gov/wp-content/uploads/2022/05/tb_summary_091922.pdf' + "\n")
    return complete_links


def get_pdf(url_list: List[str], file_name: str):
    pdf_link_list = []
    pdf_list_aux = []
    for url in url_list:
        response = requests.get(url)
        if response.status_code == 200:
            global pdf_list
            soup = BeautifulSoup(response.text, 'html.parser')
            pdf_list = soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))
        else:
            print('404 con ', url)
        pdf_list_aux.append(pdf_list)
    longitud = []

    for links in pdf_list_aux:
        longitud.append(len(links))
        if len(links) == 0:
            pdf_link_list.append('https://nodis3.gsfc.nasa.gov/npg_img/N_PR_7150_002D_/N_PR_7150_002D_.pdf')
        for link in links:
            if (link.get('href').startswith('/sites/default/files/')):
                complete_link = 'https://standards.nasa.gov' + link.get('href')
                pdf_link_list.append(complete_link)
    with open(file_name, 'w') as f:
        for element in pdf_link_list:
            f.write(element + '\n')
    print(longitud)
    return pdf_link_list


def descargar_pdf(desde_url, a_archivo):
    response = requests.get(desde_url)
    if response.status_code == 200:
        with open(a_archivo, 'wb') as archivo_local:
            archivo_local.write(response.content)
        return True
    else:
        print(f"No se pudo descargar {desde_url}")
        return False


def crear_lista_enlaces(archivo):
    with open(archivo, 'r') as f:
        lista_enlaces = f.readlines()
    lista_enlaces = [enlace.strip() for enlace in lista_enlaces]
    return lista_enlaces


def funcion_sin_nombre(enlaces_pdf):
    textos = []
    for enlace in enlaces_pdf:
        print(f"Descargando {enlace}")
        nombre_archivo = enlace.split('/')[-1]  # Obtiene el nombre del archivo desde el enlace
        if descargar_pdf(enlace, nombre_archivo):
            with open(nombre_archivo.replace(".pdf", ".txt"), 'w',encoding='utf-8') as f:
                texto = mi_funcion(nombre_archivo)
                f.write(texto)

            try:
                os.remove(nombre_archivo)
                print(f"Archivo {nombre_archivo} eliminado.")
            except OSError as e:
                print(f"No se pudo eliminar {nombre_archivo}: {e}")
    return textos


def mi_funcion(archivo_pdf):
    # Extrae el texto del PDF y almacénalo en una variable
    texto = extract_text(archivo_pdf)
    # Procesa el texto como quieras
    print(texto)
    return texto


def crear_txt(texto, nombre):
    with open(nombre, 'w', encoding='utf-8') as archivo:
        archivo.write(texto)


# standar_links = create_links(STANDAR_NAME)
# pdf_links = get_pdf(standar_links, PDF_LINKS)
# print("paso 2")
# create_file_pdfs_2('pdf2_links.txt')
# print("paso 3")
enlaces_pdf = []
enlaces_pdf += crear_lista_enlaces('pdf_links.txt')
lista_textos = funcion_sin_nombre(enlaces_pdf)
