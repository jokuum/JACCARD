import os
import json
import time

CARPETA_DOCUMENTOS = "../documentos"
ARCHIVO_INDICE = "../indice/jaccard_index.json"


def tokenizar(texto):
    texto = texto.lower().replace("\n", " ")
    palabras = [p.strip() for p in texto.split(" ")]
    return [p for p in palabras if p != ""]


def construir_indice():
    inicio = time.time()

    documentos = {}          # doc_id -> {"nombre": ..., "conjunto": [...]}
    indice_invertido = {}    # palabra -> [doc_id, doc_id, ...]

    archivos = sorted(os.listdir(CARPETA_DOCUMENTOS))
    archivos_txt = [a for a in archivos if a.endswith(".txt")]

    for nombre_archivo in archivos_txt:
        ruta = os.path.join(CARPETA_DOCUMENTOS, nombre_archivo)
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()

        doc_id = nombre_archivo.replace(".txt", "")
        tokens = tokenizar(contenido)
        conjunto_palabras = sorted(set(tokens))

        documentos[doc_id] = {
            "nombre": nombre_archivo,
            "texto": contenido,
            "conjunto": conjunto_palabras,
        }

        # Alimentar el indice invertido
        for palabra in conjunto_palabras:
            indice_invertido.setdefault(palabra, []).append(doc_id)

    resultado = {
        "documentos": documentos,
        "indice_invertido": indice_invertido,
        "total_documentos": len(documentos),
    }

    os.makedirs(os.path.dirname(ARCHIVO_INDICE), exist_ok=True)
    with open(ARCHIVO_INDICE, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    duracion = time.time() - inicio
    print(f"Indice construido con {len(documentos)} documentos")
    print(f"Vocabulario unico: {len(indice_invertido)} palabras")
    print(f"Guardado en: {ARCHIVO_INDICE}")
    print(f"Tiempo de indexacion: {duracion:.3f} segundos")


if __name__ == "__main__":
    construir_indice()