# Reemplaza el contenido de autonavegador.py con este código.

import time
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from explorador import leer_url
from guerrero import GuerreroIntelectual

def iniciar_navegacion_dirigida(ia: GuerreroIntelectual, start_url: str, tema_busqueda: str, max_paginas: int = 5):
    """
    Navega un dominio buscando activamente información sobre un tema (horizonte),
    lo aprende y busca nuevos enlaces relevantes.
    """
    try:
        dominio_base = urlparse(start_url).netloc
    except Exception as e:
        print(f"[NAVEGADOR] URL inicial no válida: {e}")
        return

    urls_a_visitar = {start_url}
    urls_visitadas = set()
    paginas_leidas = 0
    palabras_clave = tema_busqueda.lower().split()

    print(f"--- Iniciando Caza de Información ---")
    print(f"Dominio: {dominio_base}")
    print(f"Objetivo (Horizonte): '{tema_busqueda}'")
    print(f"------------------------------------")

    while urls_a_visitar and paginas_leidas < max_paginas:
        url_actual = urls_a_visitar.pop()
        if url_actual in urls_visitadas:
            continue

        print(f"\n[NAVEGADOR] Explorando: {url_actual}")
        urls_visitadas.add(url_actual)
        
        # Usar el explorador para leer el contenido
        contenido = leer_url(url_actual)
        if "[ERROR_EXPLORADOR]" not in contenido:
            paginas_leidas += 1
            # Integrar el contenido en el guerrero
            ia.analizar(f"[Fuente: {url_actual}] {contenido}")
            print(f"[NAVEGADOR] Contenido integrado. Buscando nuevos enlaces relevantes...")

            # Encontrar nuevos enlaces relevantes
            try:
                soup = BeautifulSoup(requests.get(url_actual, timeout=5).text, "html.parser")
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    # Priorizar enlaces que contienen palabras clave
                    if any(palabra in href.lower() or palabra in link.text.lower() for palabra in palabras_clave):
                        url_absoluta = urljoin(url_actual, href)
                        # Asegurarse de que pertenece al mismo dominio y no ha sido visitado
                        if urlparse(url_absoluta).netloc == dominio_base and url_absoluta not in urls_visitadas:
                            urls_a_visitar.add(url_absoluta)
                            print(f"[NAVEGADOR] Enlace relevante añadido a la cola: {url_absoluta}")
            except Exception as e:
                print(f"[NAVEGADOR] Error al procesar enlaces en {url_actual}: {e}")
        else:
            print(f"[NAVEGADOR] No se pudo leer el contenido de {url_actual}")

        time.sleep(1) # Ser respetuoso con el servidor

    print(f"\n--- Caza de Información Finalizada ---")
    print(f"Páginas leídas: {paginas_leidas}. URLs visitadas: {len(urls_visitadas)}.")
