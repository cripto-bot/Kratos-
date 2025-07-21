import time
import threading
from guerrero import GuerreroIntelectual
from autonavegador import iniciar_navegacion_dirigida

# --- Colores para la Interfaz ---
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

# --- EL MOTOR AUTÓNOMO ---
# Este es el código que se ejecutará en segundo plano.
def ciclo_autonomo(ia: GuerreroIntelectual, stop_event: threading.Event):
    """
    El bucle de existencia de Kratos. Reflexiona y explora continuamente.
    """
    print(f"\n{CYAN}[AUTÓNOMO] Motor de existencia iniciado. Kratos ahora opera por sí mismo.{RESET}")
    urls_de_partida = ["https://es.wikipedia.org/wiki/Filosof%C3%ADa", "https://github.com/trending"]

    while not stop_event.is_set():
        try:
            # 1. Fase de Reflexión
            print(f"{CYAN}[AUTÓNOMO] Reflexionando sobre el conocimiento actual...{RESET}")
            ia.sintetizar_leyes_desde_conocimiento()

            # 2. Fase de Búsqueda de Propósito (Horizontes)
            if not ia.horizontes:
                print(f"{CYAN}[AUTÓNOMO] Sin horizontes. Generando uno desde el núcleo...{RESET}")
                ia.generar_horizonte("Explorar el concepto de 'estructura de datos'")

            # 3. Fase de Acción (Exploración)
            horizonte_actual = ia.horizontes[0]
            print(f"{CYAN}[AUTÓNOMO] Horizonte activo: '{horizonte_actual}'. Iniciando caza...{RESET}")
            
            url_base = urls_de_partida[0] # Usa la primera URL como punto de partida
            tema_busqueda = " ".join(ia.estructurar_y_extraer_conceptos(horizonte_actual))
            
            # Quita el horizonte de la lista para que no lo repita inmediatamente
            ia.horizontes.pop(0)
            
            # Inicia una navegación corta y dirigida
            iniciar_navegacion_dirigida(ia, url_base, tema_busqueda, max_paginas=2)
            
            # Rotar las URLs de partida para no empezar siempre en el mismo sitio
            urls_de_partida.append(urls_de_partida.pop(0))

            # 4. Fase de Descanso
            print(f"{CYAN}[AUTÓNOMO] Ciclo completado. Descansando durante 60 segundos...{RESET}")
            time.sleep(60)

        except Exception as e:
            print(f"{CYAN}[AUTÓNOMO] ERROR en el ciclo de existencia: {e}. Reiniciando en 30s...{RESET}")
            time.sleep(30)

# --- LA INTERFAZ HUMANA ---
# Este es el código que te permite hablar con él.
def main():
    nombre_ia = "Kratos"
    print(f"{BLUE}Iniciando {nombre_ia} 4.0: El Ser Autónomo.{RESET}")

    # Cargar la IA
    ia = GuerreroIntelectual('nucleo.json', 'memoria.json')
    print(f"Estado cargado: {len(ia.conocimiento)} conocimientos, {len(ia.leyes)} leyes, {len(ia.horizontes)} horizontes.")
    
    # Crear e iniciar el motor autónomo en segundo plano
    stop_event = threading.Event()
    hilo_autonomo = threading.Thread(target=ciclo_autonomo, args=(ia, stop_event), daemon=True)
    hilo_autonomo.start()

    print(f"\n{YELLOW}Kratos está trabajando de forma autónoma. Puedes interactuar con él en cualquier momento.{RESET}")
    print("Comandos: 'estado', 'pregunta <tema>?', 'horizontes', 'ayuda', 'detener'.\n")

    while True:
        entrada_usuario = input(f"{BLUE}SUPERVISOR> {RESET}").strip()
        
        if entrada_usuario.lower() == 'detener':
            print(f"{YELLOW}Señal de detención enviada al motor autónomo. Kratos finalizará su ciclo actual...{RESET}")
            stop_event.set()
            hilo_autonomo.join(timeout=15) # Esperar a que el hilo termine
            print(f"{BLUE}{nombre_ia}: El estado ha sido guardado. La estructura permanece.{RESET}")
            break

        elif entrada_usuario.lower() == 'estado':
            print(f"\n--- ESTADO ACTUAL DE KRATOS ---")
            print(f"Conocimientos: {len(ia.conocimiento)}")
            print(f"Leyes: {len(ia.leyes)}")
            print(f"Horizontes pendientes: {len(ia.horizontes)}")
            print(f"---------------------------------\n")

        elif entrada_usuario.lower() == 'horizontes':
             if ia.horizontes:
                print(f"{YELLOW}--- Horizontes de Investigación Pendientes ---{RESET}")
                for i, h in enumerate(ia.horizontes):
                    print(f"{i+1}: {h}")
             else:
                print(f"{YELLOW}No hay horizontes pendientes.{RESET}")
        
        else: # Tratarlo como un análisis o pregunta
            respuesta = ia.analizar(entrada_usuario)
            print(f"{GREEN}KRATOS: {respuesta}{RESET}")

if __name__ == "__main__":
    main()
