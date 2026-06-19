import json
import os
from flask import Flask, render_template, request

ARCHIVO_INDICE = os.path.join("indice", "jaccard_index.json")

app = Flask(__name__)

# El indice se carga una sola vez al iniciar el servidor.
with open(ARCHIVO_INDICE, "r", encoding="utf-8") as f:
    INDICE = json.load(f)

DOCUMENTOS = INDICE["documentos"]
INDICE_INVERTIDO = INDICE["indice_invertido"]


def tokenizar(texto):
    """Misma tokenizacion que offline/indexador.py."""
    texto = texto.lower().replace("\n", " ")
    palabras = [p.strip() for p in texto.split(" ")]
    return [p for p in palabras if p != ""]


def jaccard(conjunto_a, conjunto_b):
    """J(A,B) = |A interseccion B| / |A union B|"""
    interseccion = conjunto_a & conjunto_b
    union = conjunto_a | conjunto_b
    if not union:
        return 0.0
    return len(interseccion) / len(union)


def obtener_candidatos(palabras_consulta):
    """Usa el indice invertido para comparar solo contra documentos
    que comparten al menos una palabra con la consulta."""
    candidatos = set()
    for palabra in palabras_consulta:
        candidatos.update(INDICE_INVERTIDO.get(palabra, []))
    return candidatos


def buscar(consulta_texto):
    palabras_consulta = tokenizar(consulta_texto)
    conjunto_consulta = set(palabras_consulta)

    if not conjunto_consulta:
        return []

    candidatos = obtener_candidatos(palabras_consulta)

    resultados = []
    for doc_id in candidatos:
        doc = DOCUMENTOS[doc_id]
        conjunto_doc = set(doc["conjunto"])
        score = jaccard(conjunto_consulta, conjunto_doc)
        if score > 0:
            resultados.append({
                "id": doc_id,
                "nombre": doc["nombre"],
                "texto": doc["texto"],
                "score": round(score * 100, 1),  # como porcentaje
            })

    # Resultados por relevancia
    resultados.sort(key=lambda r: r["score"], reverse=True)
    return resultados


@app.route("/", methods=["GET"])
def index():
    consulta = request.args.get("q", "").strip()
    resultados = buscar(consulta) if consulta else []
    return render_template(
        "index.html",
        consulta=consulta,
        resultados=resultados,
        total_documentos=INDICE["total_documentos"],
    )


if __name__ == "__main__":
    app.run(debug=True)