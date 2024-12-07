import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

def cochista(ruta="cochesNet.csv", paginas=1):
    start = time.time()
    
    desktop_agents = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
    ]


    # Encabezados para la solicitud HTTP
    headers = {
        "User-Agent": random.choice(desktop_agents),
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive", 
        "Referer": "https://www.coches.net/",
    }
    
    # Columnas del archivo CSV
    columns = ["Titulo", "Marca", "Precio", "Provincia", "Motor", "Año", "Kilometros", "Link"]
    df = pd.DataFrame(columns=columns)
    df.to_csv(ruta, index=False, mode='w', sep=",", header=True)
    print(paginas)
    for counter in range(1, paginas + 1): #Hacer con while true mas tarde
        url = f"https://www.coches.net/search/?MakeIds%5B0%5D=1354&ModelIds%5B0%5D=0&Versions%5B0%5D=&pg={counter}"
        print(f"Scraping página: {url}")
        
        # Solicitud HTTP
        response = requests.get(url, headers=headers)
        time.sleep(random.uniform(2, 5)) #Por que COÑO solo aparecen los 2 primeros de cada pagina xd?
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Bloques de anuncios
        bloques = soup.select(".mt-ListAds > div[data-ad-id]")
        
        for bloque in bloques:
            # Extraer título
            titulo_elem = bloque.select_one(".mt-CardBasic-titleLink")
            titulo = titulo_elem["title"] if titulo_elem else None
            
            # Marca (extraída del título)
            marca = titulo.split(" ")[0] if titulo else None
            
            # Precio
            precio_elem = bloque.select_one(".mt-CardAdPrice-cashAmount h3")
            precio = precio_elem.get_text(strip=True).replace("€", "").replace(".", "").strip() if precio_elem else None
            precio = int(precio) if precio and precio.isdigit() else None
            
            # Provincia
            prov_elem = bloque.select_one(".mt-CardAd-attr li:nth-child(1)")
            provincia = prov_elem.get_text(strip=True) if prov_elem else None
            
            # Motor
            motor_elem = bloque.select_one(".mt-CardAd-attr li:nth-child(2)")
            motor = motor_elem.get_text(strip=True) if motor_elem else None
            
            # Año
            año_elem = bloque.select_one(".mt-CardAd-attr li:nth-child(3)")
            año = año_elem.get_text(strip=True) if año_elem else None
            
            # Kilómetros
            km_elem = bloque.select_one(".mt-CardAd-attr li:nth-child(4)")
            km = km_elem.get_text(strip=True) if km_elem else None
            
            # Link
            link_elem = bloque.select_one(".mt-CardBasic-titleLink")
            link = f"https://www.coches.net{link_elem['href']}" if link_elem and 'href' in link_elem.attrs else None
            
            print(titulo, marca, precio, provincia, motor, año, km, link)
            
            # Guardamos en un .csv
            line = pd.DataFrame([[titulo, marca, precio, provincia, motor, año, km, link]], columns=columns)
            line.to_csv(ruta, index=False, mode='a', sep=",", header=False)

    end = time.time()
    print(f"Scraping completado en {end - start:.2f} segundos")

# Llamar a la función con maximo de paginaas supongo?
cochista(paginas=20)
