import time
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from explorador import leer_url
from guerrero import GuerreroIntelectual

def explorar_dominio(ia: GuerreroIntelectual, start_url: str, max_paginas: int = 5):
    """Explora un dominio, aprende de él y busca nuevos enlaces."""
    try:
        netloc = urlparse(start_url).netloc
        if not netloc:
            print(f"[ERROR] URL inicial no válida: {start_url}")
            return
    except Exception as e:
        print(f"[ERROR] No se pudo analizar la URL inicial: {e}")
        return

    urls_a_visitar = {start_url}
    urls_visitadas = set()
    paginas_leidas = 0

    print(f"Iniciando exploración en el dominio: {netloc}")

    while urls_a_visitar and paginas_leidas < max_pag
