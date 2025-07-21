import requests
from bs4 import BeautifulSoup

def leer_url(url: str, max_chars: int = 2000) -> str:
    try:
        headers = {"User-Agent": "Kratos-Structural-Agent/1.0"}
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        texto_limpio = ' '.join(soup.get_text().split())
        return texto_limpio[:max_chars]
    except requests.exceptions.RequestException as e:
        return f"[ERROR_EXPLORADOR] No se pudo leer {url}: {e}"
