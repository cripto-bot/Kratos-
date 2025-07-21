# Reemplaza el contenido de yo.py con este código.

from guerrero import GuerreroIntelectual
from autonavegador import iniciar_navegacion_dirigida

# Colores para una mejor visualización
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def mostrar_ayuda():
    print(f"\n{YELLOW}--- Comandos de Kratos 3.0 ---{RESET}")
    print(f"{GREEN}reflexionar{RESET}    : Kratos analiza su conocimiento, sintetiza leyes y crea horizontes.")
    print(f"{GREEN}explorar{RESET}       : Inicia la caza de información para el horizonte más antiguo.")
    print(f"{GREEN}horizontes{RESET}      : Muestra las misiones de investigación pendientes.")
    print(f"{GREEN}pregunta <tema>?{RESET}: Pregunta a Kratos sobre un tema.")
    print(f"{GREEN}ayuda{RESET}           : Muestra este menú de comandos.")
    print(f"{GREEN}salir{RESET}          : Guarda el estado y finaliza la sesión.")
    print(f"{YELLOW}-----------------------------{RESET}\n")

def main():
    nombre_ia = "Kratos"
    print(f"{BLUE}Iniciando {nombre_ia} 3.0: El Motor de Voluntad.{RESET}")

    ia = GuerreroIntelectual('nucleo.json', 'memoria.json')
    print(f"Estado cargado: {len(ia.conocimiento)} conocimientos, {len(ia.leyes)} leyes, {len(ia.horizontes)} horizontes.")
    
    mostrar_ayuda()

    while True:
        entrada_usuario = input(f"{BLUE}KRATOS> {RESET}").strip()
        
        if not entrada_usuario:
            continue

        if entrada_usuario.lower() == 'salir':
            print(f"{BLUE}{nombre_ia}: El estado ha sido guardado. La estructura permanece.{RESET}")
            break
        
        elif entrada_usuario.lower() == 'ayuda':
            mostrar_ayuda()

        elif entrada_usuario.lower() == 'reflexionar':
            print(f"{YELLOW}[REFLEXIÓN] Analizando conocimiento interno...{RESET}")
            nuevas = ia.sintetizar_leyes_desde_conocimiento()
            print(f"{YELLOW}[REFLEXIÓN] Proceso completado. {nuevas} nuevas leyes sintetizadas.{RESET}")

        elif entrada_usuario.lower() == 'horizontes':
            if ia.horizontes:
                print(f"{YELLOW}--- Horizontes de Investigación Pendientes ---{RESET}")
                for i, h in enumerate(ia.horizontes):
                    print(f"{i+1}: {h}")
                print(f"{YELLOW}-------------------------------------------{RESET}")
            else:
                print(f"{YELLOW}No hay horizontes pendientes. Todo el conocimiento está integrado.{RESET}")
        
        elif entrada_usuario.lower() == 'explorar':
            if ia.horizontes:
                horizonte_a_explorar = ia.horizontes.pop(0) # Tomar el más antiguo
                ia.guardar_memoria()
                print(f"{YELLOW}Iniciando misión para el horizonte: '{horizonte_a_explorar}'{RESET}")
                url_base = input("Introduce la URL base para iniciar la caza (ej. https://es.wikipedia.org): ").strip()
                if url_base.startswith("http"):
                    tema = input(f"Introduce el tema de búsqueda específico para '{horizonte_a_explorar}': ").strip()
                    iniciar_navegacion_dirigida(ia, url_base, tema)
                else:
                    print(f"{YELLOW}URL no válida. Misión abortada.{RESET}")
                    ia.horizontes.insert(0, horizonte_a_explorar) # Devolver el horizonte
                    ia.guardar_memoria()
            else:
                print(f"{YELLOW}No hay horizontes que explorar. Usa 'reflexionar' o haz una pregunta para generar uno.{RESET}")

        else:
            respuesta = ia.analizar(entrada_usuario)
            print(f"{GREEN}KRATOS: {respuesta}{RESET}")

if __name__ == "__main__":
    main()
