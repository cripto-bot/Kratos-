# curador.py

import json
import sys

MEMORIA_PATH = 'memoria.json'

def cargar_memoria():
    try:
        with open(MEMORIA_PATH, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error: No se pudo leer o decodificar {MEMORIA_PATH}.")
        return None

def guardar_memoria(datos):
    with open(MEMORIA_PATH, 'w') as f:
        json.dump(datos, f, indent=2)
    print("Memoria actualizada y guardada con éxito.")

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 curador.py [comando] [argumento]")
        print("Comandos:")
        print("  ver <seccion>           (seccion: conocimiento, leyes, horizontes, registro)")
        print("  add-conocimiento \"texto\"")
        print("  limpiar-registro")
        return

    comando = sys.argv[1]
    memoria = cargar_memoria()
    if memoria is None:
        return

    if comando == 'ver' and len(sys.argv) > 2:
        seccion = sys.argv[2]
        if seccion in memoria:
            print(json.dumps(memoria[seccion], indent=2))
        else:
            print(f"Error: La sección '{seccion}' no existe.")

    elif comando == 'add-conocimiento' and len(sys.argv) > 2:
        nuevo_conocimiento = sys.argv[2]
        if nuevo_conocimiento not in memoria['conocimiento']:
            memoria['conocimiento'].append(nuevo_conocimiento)
            guardar_memoria(memoria)
        else:
            print("El conocimiento ya existe en la memoria.")
            
    elif comando == 'limpiar-registro':
        memoria['registro'] = []
        guardar_memoria(memoria)
        
    else:
        print(f"Comando '{comando}' no reconocido o argumentos insuficientes.")

if __name__ == '__main__':
    main()
