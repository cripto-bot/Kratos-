import time
from explorador import leer_url
from guerrero import GuerreroIntelectual

def iniciar_navegacion_autonoma(ia: GuerreroIntelectual):
    URLS_A_EXPLORAR = [
        "https://es.wikipedia.org/wiki/Estoicismo",
        "https://es.wikipedia.org/wiki/Lógica",
        "https://raw.githubusercontent.com/python/cpython/main/README.rst"
    ]
    
    print("Iniciando ciclo de aprendizaje autónomo...")
    for u in URLS_A_EXPLORAR:
        print(f"→ Explorando: {u}")
        contenido = leer_url(u)
        fragmento = f"El contenido de '{u}' menciona: {contenido[:500]}"
        resultado = ia.analizar(fragmento)
        print(f"  └ Resultado: {resultado}")
        time.sleep(2)
    
    print("\nCiclo de navegación completado.")
