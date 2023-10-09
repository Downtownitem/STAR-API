import requests


url = "https://ntrs.nasa.gov/api/v1/search"


params = {
    "q": "space",
    "fl": "title,author,pubDate",
    "rows": 10  
}


response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()

    for document in data["response"]["docs"]:
        print(f"Título: {document['title'][0]}")
        print(f"Autor: {document.get('author', ['Desconocido'])[0]}")
        print(f"Fecha de publicación: {document.get('pubDate', 'Desconocida')}")
        print("\n---\n")
else:
    print(f"La solicitud falló con el código de estado: {response.status_code}")
