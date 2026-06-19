import os
import random

TEMAS = {
    "tecnologia": [
        "python", "java", "software", "internet", "datos", "red", "computadora",
        "programa", "codigo", "sistema", "servidor", "base", "algoritmo",
        "inteligencia", "artificial", "robot", "pantalla", "teclado", "mouse",
        "archivo", "carpeta", "nube", "aplicacion", "celular", "telefono",
        "tablet", "impresora", "memoria", "procesador", "navegador",
    ],
    "deporte": [
        "futbol", "basquetbol", "tenis", "natacion", "atletismo", "ciclismo",
        "voleibol", "golf", "boxeo", "karate", "yoga", "gimnasio", "pelota",
        "cancha", "estadio", "equipo", "jugador", "entrenador", "medalla",
        "campeonato", "torneo", "carrera", "maraton", "bicicleta", "raqueta",
    ],
    "comida": [
        "pizza", "pasta", "arroz", "pollo", "carne", "pescado", "ensalada",
        "sopa", "pan", "queso", "leche", "huevo", "fruta", "verdura", "postre",
        "chocolate", "cafe", "te", "jugo", "agua", "vino", "cerveza",
        "restaurante", "cocina", "receta", "ingrediente", "sabor",
    ],
    "viaje": [
        "avion", "barco", "tren", "auto", "bus", "maleta", "pasaporte",
        "hotel", "playa", "montana", "ciudad", "pueblo", "turista", "mapa",
        "boleto", "aeropuerto", "vacaciones", "aventura", "cultura", "idioma",
        "moneda", "paisaje", "fotografia", "recuerdo", "guia", "excursion",
    ],
    "ciencia": [
        "atomo", "molecula", "celula", "genetica", "fisica", "quimica",
        "biologia", "matematica", "universo", "planeta", "estrella",
        "galaxia", "experimento", "laboratorio", "microscopio", "telescopio",
        "teoria", "hipotesis", "investigacion", "cientifico", "descubrimiento",
        "energia", "materia", "fuerza", "gravedad",
    ],
    "musica": [
        "guitarra", "piano", "violin", "bateria", "cancion", "melodia",
        "ritmo", "concierto", "banda", "orquesta", "cantante", "musico",
        "instrumento", "album", "disco", "letra", "acorde", "nota",
        "partitura", "escenario", "publico", "festival", "sonido",
    ],
    "negocios": [
        "empresa", "mercado", "venta", "cliente", "producto", "servicio",
        "inversion", "finanzas", "presupuesto", "ganancia", "perdida",
        "estrategia", "gerente", "empleado", "oficina", "reunion", "proyecto",
        "meta", "objetivo", "competencia", "marca", "publicidad", "contrato",
    ],
    "educacion": [
        "escuela", "universidad", "profesor", "estudiante", "clase", "examen",
        "tarea", "libro", "biblioteca", "aula", "pizarra", "leccion", "curso",
        "carrera", "titulo", "diploma", "investigacion", "tesis",
        "conocimiento", "aprendizaje", "ensenanza", "pregunta", "respuesta",
    ],
}

CONECTORES = [
    "de", "la", "el", "en", "y", "un", "una", "que", "con", "por", "para",
    "los", "las", "su", "es", "se", "no", "mas", "como", "pero", "muy",
]

def generar_linea(palabras_tema, min_palabras=6, max_palabras=11):
    """Genera una linea mezclando palabras del tema con conectores."""
    n = random.randint(min_palabras, max_palabras)
    linea = []
    for _ in range(n):
        if random.random() < 0.65:
            linea.append(random.choice(palabras_tema))
        else:
            linea.append(random.choice(CONECTORES))
    return " ".join(linea)

def generar_documento(tema):
    palabras_tema = TEMAS[tema]
    num_lineas = random.randint(2, 4)
    lineas = [generar_linea(palabras_tema) for _ in range(num_lineas)]
    return "\n".join(lineas)

def main(cantidad=200, salida="../documentos", semilla=42):
    random.seed(semilla)  
    os.makedirs(salida, exist_ok=True)

    temas_lista = list(TEMAS.keys())
    resumen = {tema: 0 for tema in temas_lista}

    for i in range(1, cantidad + 1):
        tema = random.choice(temas_lista)
        contenido = generar_documento(tema)
        nombre_archivo = f"doc_{i:03d}.txt"
        ruta = os.path.join(salida, nombre_archivo)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        resumen[tema] += 1

    print(f"Se generaron {cantidad} documentos en '{salida}'")
    print("Distribucion por tema:") 
    for tema, n in resumen.items():
        print(f"  - {tema}: {n} documentos")


if __name__ == "__main__":
    main()