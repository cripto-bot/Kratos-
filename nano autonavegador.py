import time
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from explorador import leer_url
from guerrero import GuerreroIntelectual

def iniciar_navegacion_dirigida(ia: GuerreroIntelectual, start_url: str, tema_busqueda: str, max_paginas: int = 3):
    """
    Navega un dominio, busca información sobre un tema y CAZA nuevos dominios prometedores.
    Devuelve una lista de nuevos dominios encontrados.
    """
    try:
        dominio_base = urlparse(start_url).netloc
    except Exception as e:
        print(f"[NAVEGADOR] URL inicial no válida: {e}")
        return []

    urls_a_visitar = {start_url}
    urls_visitadas = set()
    nuevas_fuentes_prometedoras = set()
    palabras_clave_prometedoras = ['research', 'edu', 'gov', 'org', 'docs', 'paper', 'article']

    while urls_a_visitar and len(urls_visitadas) < max_paginas:
        url_actual = urls_a_visitar.pop()
        if url_actual in urls_visitadas:
            continue
        
        print(f"[NAVEGADOR] Explorando: {url_actual}")
        urls_visitadas.add(url_actual)
        
        contenido = leer_url(url_actual)
        if "[ERROR_EXPLORADOR]" not in contenido:
            ia.analizar(f"[Fuente: {url_actual}] {contenido}")
            
            try:
                soup = BeautifulSoup(requests.get(url_actual, timeout=5).text, "html.parser")
                for link in soup.find_all('a', href=True):
                    url_absoluta = urljoin(url_actual, link['href'])
                    nuevo_dominio = urlparse(url_absoluta).netloc
                    
                    if nuevo_dominio and nuevo_dominio != dominio_base:
                        # Evaluar si la nueva fuente es prometedora
                        if any(palabra in nuevo_dominio or palabra in url_absoluta for palabra in palabras_clave_prometedoras):
                            if url_absoluta not in nuevas_fuentes_prometedoras:
                                print(f"[CAZADOR DE FUENTES] Nuevo dominio prometedor encontrado: {url_absoluta}")
                                nuevas_fuentes_prometedoras.add(url_absoluta)
                    elif nuevo_dominio == dominio_base and url_absoluta not in urls_visitadas:
                        urls_a_visitar.add(url_
