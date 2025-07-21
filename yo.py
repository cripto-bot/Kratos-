from guerrero import GuerreroIntelectual
from autonavegador import iniciar_navegacion_autonoma

GREEN = "\033[32m"
RESET = "\033[0m"

def main():
    nombre_ia = "Kratos"
    print(f"Iniciando {nombre_ia}...")

    ia = GuerreroIntelectual('nucleo.json', 'memoria.json')
    print(f"{nombre_ia} ha cargado sus principios y memoria ({len(ia.conocimiento)} conocimientos, {len(ia.leyes)} leyes).")
    print("Comandos: 'navegar', 'salir', o introduce conocimiento.\n")

    while True:
        entrada_usuario = input("> ").strip()
        if entrada_usuario.lower() == 'salir':
            print(f"{nombre_ia}: Estado guardado. La estructura permanece.")
            break
        
        if entrada_usuario.lower() == 'navegar':
            print(f"{GREEN}{nombre_ia}: Iniciando proceso de navegación autónoma...{RESET}")
            iniciar_navegacion_autonoma(ia)
            print(f"{GREEN}{nombre_ia}: Proceso de navegación finalizado.{RESET}")
        else:
            respuesta = ia.analizar(entrada_usuario)
            print(f"{GREEN}{nombre_ia}: {respuesta}{RESET}")

if __name__ == "__main__":
    main()
