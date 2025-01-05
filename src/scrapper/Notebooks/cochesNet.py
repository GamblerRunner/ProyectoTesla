from random import uniform as num_uniforme
from bs4 import BeautifulSoup
from seleniumbase import SB
import pdb
import pandas as pd

class AnuncioVehiculo:
    def __init__(self, titulo, precio, ubicacion, tipo_vehiculo, ano, kilometraje, enlace):
        self.titulo = titulo
        self.precio = precio
        self.ubicacion = ubicacion
        self.tipo_vehiculo = tipo_vehiculo
        self.ano = ano
        self.kilometraje = kilometraje
        self.enlace = enlace

    def __str__(self):
        return f'''
        Título: {self.titulo}
        Precio: {self.precio}
        Ubicación: {self.ubicacion}
        Tipo de vehículo: {self.tipo_vehiculo}
        Año: {self.ano}
        Kilometraje: {self.kilometraje}
        Enlace: {self.enlace}
        '''
    
    def __eq__(self, other):
        if isinstance(other, AnuncioVehiculo):
            return (self.titulo == other.titulo and self.enlace == other.enlace)
        return False

    def __hash__(self):
        return hash((self.titulo, self.enlace))
    
    def to_dict(self):
        return {
            "Titulo": self.titulo,
            "Precio": self.precio,
            "Ubicación": self.ubicacion,
            "Tipo de vehículo": self.tipo_vehiculo,
            "Año": self.ano,
            "Kilometros": self.kilometraje,
            "Link": self.enlace
        }
    
def html_to_av(html_code) -> AnuncioVehiculo:
    soup = BeautifulSoup(html_code, 'html.parser')

    titulo = soup.find('h2', class_='mt-CardAd-infoHeaderTitle').text.strip()
    precio = soup.find('h3', class_='mt-TitleBasic-title').text.strip()
    ubicacion = soup.find_all('li', class_='mt-CardAd-attrItem')[0].text.strip()
    tipo_vehiculo = soup.find_all('li', class_='mt-CardAd-attrItem')[1].text.strip()
    ano = soup.find_all('li', class_='mt-CardAd-attrItem')[2].text.strip()
    kilometraje = soup.find_all('li', class_='mt-CardAd-attrItem')[3].text.strip()
    enlace = soup.find('a', class_='mt-CardBasic-titleLink')['href']

    return AnuncioVehiculo(titulo, precio, ubicacion, tipo_vehiculo, ano, kilometraje, enlace)

count = 0

with SB(
    uc=True,
    test=True, 
    headless=True,
    ad_block=True,
) as sb:
    arry_coches = []
    columns = ["Titulo", "Precio", "Ubicación", "Tipo de vehículo", "Año", "Kilometros", "Link"]
    df = pd.DataFrame(columns=columns)
    for num_pag in range(19):
        try:
            sb.activate_cdp_mode(f'https://www.coches.net/search/?MakeIds[0]=1354&ModelIds[0]=0&Versions[0]=&pg={num_pag}')
            if num_pag == 0:
                sb.cdp.click('#didomi-notice-agree-button', timeout=20)
            sb.sleep(num_uniforme(4.00, 6.30))
            for elm in sb.cdp.find_all('.mt-ListAds > div[data-ad-position]'):
                try:
                    elm.scroll_into_view()
                    sb.sleep(0.35)
                    arry_coches.append(html_to_av(elm.get_html()))
                except Exception:
                    pass
            count += len(arry_coches)
            print(f"Coches obtenidos actualmente: {count}")
        except Exception:
            pass
        num_pag -= 1

    arry_coches_sin_duplicados = list(set(arry_coches))

    # Convertir a lista de diccionarios
    datos = [coche.to_dict() for coche in arry_coches_sin_duplicados]

    # Crear el DataFrame
    line = pd.DataFrame(datos, columns=columns)

    #line = pd.DataFrame(arry_coches_sin_duplicados, columns=columns)
    ruta="../../../data/cochesNet.csv"
    line.to_csv(ruta, index=False, mode='a', sep=",")

    # pdb.set_trace()