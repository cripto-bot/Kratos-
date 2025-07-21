# Reemplaza el contenido de guerrero.py con este código actualizado.
# Los cambios clave son la adición de `generar_horizonte` y
# la modificación de `analizar` para usarlo.

import json
import uuid
from typing import List

class Ley:
    # ... (El código de la clase Ley no cambia)
    def __init__(self, descripcion: str, condiciones: List[str], conclusion: str, id: str = None):
        self.id = id or str(uuid.uuid4())
        self.descripcion = descripcion
        self.condiciones = condiciones
        self.conclusion = conclusion

    def aplica(self, contexto: List[str]) -> bool:
        return any(any(cond in c_item.lower() for c_item in contexto) for cond in self.condiciones)

class GuerreroIntelectual:
    # ... (__init__, cargar_memoria, guardar_memoria no cambian)
    def __init__(self, ruta_nucleo: str, ruta_memoria: str):
        self.ruta_nucleo = ruta_nucleo
        self.ruta_memoria = ruta_memoria
        with open(self.ruta_nucleo, 'r') as f:
            self.nucleo = json.load(f)
        self.cargar_memoria()

    def cargar_memoria(self):
        try:
            with open(self.ruta_memoria, 'r') as m_file:
                m = json.load(m_file)
            self.conocimiento = m.get("conocimiento", [])
            self.leyes = [Ley(**l_data) for l_data in m.get("leyes", [])]
            self.horizontes = m.get("horizontes", [])
            self.registro = m.get("registro", [])
        except (FileNotFoundError, json.JSONDecodeError):
            self.conocimiento = []
            self.leyes = []
            self.horizontes = []
            self.registro = []
            self.guardar_memoria()

    def guardar_memoria(self):
        datos = {
            "conocimiento": self.conocimiento,
            "leyes": [vars(l) for l in self.leyes],
            "horizontes": self.horizontes,
            "registro": self.registro
        }
        with open(self.ruta_memoria, 'w') as f:
            json.dump(datos, f, indent=2)

    def analizar(self, entrada: str) -> str:
        self.registro.append(f"ANALIZANDO: {entrada[:100]}...")
        e = entrada.strip()

        # Si es una pregunta, intenta responderla o crea un horizonte
        if e.endswith('?'):
            respuesta = self.preguntar(e[:-1])
            if respuesta:
                return f"Respuesta basada en conocimiento actual: {respuesta}"
            else:
                self.generar_horizonte(f"Investigar respuesta a la pregunta: {e}")
                return "No tengo conocimiento directo. Se ha creado un horizonte de investigación."

        # ... (el resto de la lógica de analizar no cambia)
        if " si " in e.lower() and " entonces " in e.lower():
            return self._procesar_ejemplo(e)
        if self.nucleo.get("estructura_tecnica_valida") and any(k in e for k in ["def ", "class ", "import ", "git "]):
            if f"[TÉCNICO] {e}" not in self.conocimiento:
                self.conocimiento.append(f"[TÉCNICO] {e}")
                self.guardar_memoria()
            return "Conocimiento técnico integrado."
        if self.nucleo.get("contradiccion_invalida"):
            for c in self.conocimiento:
                if f"no {c}" == e or c == f"no {e}":
                    return "Contradicción detectada. No integrado."
        if e not in self.conocimiento:
            self.conocimiento.append(e)
            self.guardar_memoria()
        
        return "Entrada coherente. Integrada."

    # >>> NUEVA FUNCIÓN: CONCIENCIA DE LA IGNORANCIA <<<
    def generar_horizonte(self, tema: str):
        """Añade un tema de investigación a la lista de horizontes si no existe ya."""
        if tema not in self.horizontes:
            self.horizontes.append(tema)
            self.guardar_memoria()
            print(f"[HORIZONTE CREADO] Nueva misión: {tema}")

    def _procesar_ejemplo(self, e: str) -> str:
        try:
            partes = e.lower().split(" si ", 1)[1].split(" entonces ")
            cond = partes[0].strip()
            concl = partes[1].strip()
            nueva_ley = Ley(f"Regla de ejemplo: {cond}", [cond], concl)
            self.leyes.append(nueva_ley)
            self.guardar_memoria()
            return "Ley extraída desde ejemplo e integrada."
        except Exception:
            if e not in self.conocimiento:
                self.conocimiento.append(e)
                self.guardar_memoria()
            return "Ejemplo complejo registrado como conocimiento fáctico."

    def preguntar(self, tema: str) -> list:
        tema_lower = tema.lower()
        # Mejora: la respuesta es más específica
        resultados = [k for k in self.conocimiento if tema_lower in k.lower()]
        return resultados

    # ... (estructurar_y_extraer_conceptos y sintetizar_leyes_desde_conocimiento no cambian)
    def estructurar_y_extraer_conceptos(self, texto: str) -> list:
        palabras = texto.lower().split()
        conceptos_comunes = [p.strip(".,:;()") for p in palabras if len(p) > 5 and p.isalpha()]
        frecuencia = {c: conceptos_comunes.count(c) for c in set(conceptos_comunes)}
        conceptos_ordenados = sorted(frecuencia.keys(), key=lambda x: frecuencia[x], reverse=True)
        return conceptos_ordenados[:5]

    def sintetizar_leyes_desde_conocimiento(self) -> int:
        if len(self.conocimiento) < 3:
            return 0
        todo_el_texto = " ".join(self.conocimiento).lower()
        conceptos_clave = self.estructurar_y_extraer_conceptos(todo_el_texto)
        nuevas_leyes_creadas = 0
        if len(conceptos_clave) >= 2:
            c1, c2 = conceptos_clave[0], conceptos_clave[1]
            nueva_ley_desc = f"Ley Sintetizada: Existe una posible relación entre '{c1}' y '{c2}'."
            if not any(ley.descripcion == nueva_ley_desc for ley in self.leyes):
                ley_sintetizada = Ley(nueva_ley_desc, [c1], c2)
                self.leyes.append(ley_sintetizada)
                print(f"[SÍNTESIS] Nueva ley creada: {nueva_ley_desc}")
                nuevas_leyes_creadas += 1
        if nuevas_leyes_creadas > 0:
            self.guardar_memoria()
        return nuevas_leyes_creadas
