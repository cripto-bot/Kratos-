import json
import uuid
from typing import List

class Ley:
    def __init__(self, descripcion: str, condiciones: List[str], conclusion: str, id: str = None):
        self.id = id or str(uuid.uuid4())
        self.descripcion = descripcion
        self.condiciones = condiciones
        self.conclusion = conclusion

    def aplica(self, contexto: List[str]) -> bool:
        return all(condicion in contexto for condicion in self.condiciones)

class GuerreroIntelectual:
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
