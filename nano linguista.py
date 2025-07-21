import spacy
from typing import Dict, Optional

class AnalizadorLinguistico:
    def __init__(self):
        """Carga el modelo de lenguaje de spaCy."""
        try:
            # Carga el modelo pequeño y eficiente en español
            self.nlp = spacy.load("es_core_news_sm")
            print("[LINGUISTA] Modelo 'es_core_news_sm' cargado. Visión estructural activada.")
        except OSError:
            print("[LINGUISTA-ERROR] El modelo de lenguaje 'es_core_news_sm' no está instalado.")
            print("                Por favor, ejecute en la terminal: python3 -m spacy download es_core_news_sm")
            self.nlp = None

    def descomponer_en_hecho_logico(self, oracion: str) -> Optional[Dict[str, any]]:
        """
        Analiza una oración y la descompone en sus componentes lógicos:
        Agente (quién hace), Acción (qué hace) y Paciente (a quién/qué se lo hace).
        """
        if not self.nlp:
            return None

        # Procesa la oración para crear un objeto 'doc' con todo el análisis
        doc = self.nlp(oracion)
        
        verbo_raiz = None
        for token in doc:
            # El "ROOT" es el núcleo de la dependencia gramatical, usualmente el verbo
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                verbo_raiz = token
                break

        # Si no hay un verbo como raíz, la oración no es una acción clara. Se descarta.
        if not verbo_raiz:
            return None

        # --- Extracción Estructural ---
        
        # El sujeto nominal (nsubj) es el Agente de la acción
        sujetos = [hijo.text for hijo in verbo_raiz.children if hijo.dep_ == "nsubj"]
        agente = sujetos[0] if sujetos else "indeterminado"

        # El objeto directo (dobj) es el Paciente de la acción
        objetos_directos = [hijo.text for hijo in verbo_raiz.children if hijo.dep_ == "obj"]
        paciente = objetos_directos[0] if objetos_directos else None
        
        # --- Construcción del Hecho Lógico ---
        # Usamos el 'lema' del verbo (su forma base: "estructurando" -> "estructurar")
        hecho_logico = {
            "agente": agente,
            "accion": verbo_raiz.lemma_,
            "paciente": paciente,
            "fuente_original": oracion
        }

        # Filtro de calidad: no guardar hechos donde no se pudo determinar ni el agente ni el paciente.
        if hecho_logico["agente"] == "indeterminado" and not hecho_logico["paciente"]:
            return None

        return hecho_logico
