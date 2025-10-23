import bibtexparser
import pandas as pd
import pycountry
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from matplotlib.backends.backend_pdf import PdfPages
import os
import requests
import re
from pathlib import Path
from typing import List, Dict
from django.conf import settings

#Obtenemos el pais desde el doi
def pais_desde_doi(doi: str) -> str:
    if not doi:
        return "Desconocido"
    url = f"https://api.crossref.org/works/{doi}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return "Desconocido"
        data = response.json().get("message", {})
        autores = data.get("author", [])
        if not autores:
            return "Desconocido"
        for autor in autores :
            afiliaciones = autor.get("affiliation", [])
            if not afiliaciones:
                return "Desconocido"
            texto = afiliaciones[0].get("name", "").lower()
        for pais in pycountry.countries:
            if re.search(rf"\b{re.escape(pais.name.lower())}\b", texto):
                return pais.name
        return "Desconocido"
    except Exception:
        return "Desconocido"


def data_from_bibtext(path: str):
    # Leer archivo BibTeX
    with open(path, encoding="utf-8") as bibfile:
        content = bibfile.read()
        bib_database = bibtexparser.parse_string(content)

    # Extraer datos
    datos = []
    for entry in bib_database.entries:
        # Convertimos los objetos Field a un diccionario legible
        if hasattr(entry, "fields"):
            fields = {f.key: f.value for f in entry.fields}
        else:
            fields = {}

        # Obtener autores
        autores = fields.get("author", "").split(" and ")
        primero = autores[0].split(",")[0].strip() if autores and autores[0] else ""

        # Obtener DOI y país
        doi = fields.get("doi", "").strip()
        pais = pais_desde_doi(doi)  # <-- tu función externa

        # Mostrar log en consola
        print(f"{doi} → {pais}")

        # Agregar fila al DataFrame
        datos.append({
            "autor": primero,
            "pais": pais,
            "año": fields.get("year", ""),
            "revista": fields.get("booktitle", fields.get("journal", "Desconocida")),
            "abstract": fields.get("abstract", ""),
            "keywords": fields.get("keywords", "")
        })

    # Convertir a DataFrame y retornarlo
    df = pd.DataFrame(datos)
    
    #os.makedirs("static/mi_app/imagenes", exist_ok=True)
    heat_map(df)
    cloud_words(df)
    temporal_line(df)
    export()



# 3. Mapa de calor (conteo por país)
def normalize_country(name):
    if not name or str(name).strip().lower() in ("desconocido", ""):
        return "Desconocido"
    try:
        return pycountry.countries.lookup(name).name
    except Exception:
        alt = {"USA": "United States of America", "US": "United States of America",
               "UK": "United Kingdom", "China": "China"}
        return alt.get(name, name)

#cargamos la informacion para crear el mapa
def load_world_geodata(cache_path="data/countries.geojson"):
    #os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    if os.path.exists(cache_path):
        return gpd.read_file(cache_path)
    url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    with open(cache_path, "wb") as fh:
        fh.write(resp.content)
    return gpd.read_file(cache_path)

#creamos el mapa de calor
def heat_map(df: pd.DataFrame):

    df = df.copy()
    df["pais"] = df["pais"].fillna("Desconocido").apply(normalize_country)
    counts = df["pais"].value_counts()

    known = counts[counts.index != "Desconocido"]
    if not known.empty:
        try:
            world = load_world_geodata()
        except Exception as e:
            # Fallback a gráfico de barras si falla la carga del GeoJSON
            fig, ax = plt.subplots(figsize=(10, 5))
            counts.plot(kind="bar", color="orange", ax=ax)
            ax.set_xlabel("País")
            ax.set_ylabel("Cantidad de artículos")
            ax.set_title("Distribución geográfica por primer autor (fallback por error en GeoData)")
            fig.savefig("imagenes/mapa_de_calor.png",dpi=300, bbox_inches="tight")
            plt.close(fig)
            return

        # Determinar nombre de columna con nombres de país
        candidate_cols = [c for c in ["ADMIN", "ADMINISTRAT", "NAME", "name"] if c in world.columns]
        name_col = candidate_cols[0] if candidate_cols else world.columns[0]

        mapping = {name: int(cnt) for name, cnt in known.items()}
        world = world.copy()
        world["count"] = world[name_col].map(mapping).fillna(0)

        fig, ax = plt.subplots(1, 1, figsize=(14, 7))
        world.plot(column="count", cmap="OrRd", linewidth=0.3, ax=ax, edgecolor="0.8", legend=True)
        ax.set_title("Distribución geográfica por primer autor")
        ax.set_axis_off()
        fig.savefig(
            os.path.join(settings.BASE_DIR, "mi_app/static/mi_app/imagenes/mapa_de_calor.jpg"),
            dpi=400, pil_kwargs={"quality": 95},  bbox_inches="tight")
        plt.close(fig)
    else:
        # Fallback: barra simple si no hay países geolocalizados
        fig, ax = plt.subplots(figsize=(10, 5))
        counts.plot(kind="bar", color="orange", ax=ax)
        ax.set_xlabel("País")
        ax.set_ylabel("Cantidad de artículos")
        ax.set_title("Distribución geográfica por primer autor (fallback)")
        fig.savefig("static/mi_app/imagenes/mapa_de_calor.png", bbox_inches="tight")
        plt.close(fig)

#creamos la nube de palabras
def cloud_words(df: pd.DataFrame):
    texto = " ".join(df["abstract"].fillna("") + " " + df["keywords"].fillna(""))
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(texto)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Nube de palabras")
    plt.tight_layout()
    plt.savefig(
        os.path.join(settings.BASE_DIR, "mi_app/static/mi_app/imagenes/nube_de_palabras.jpg"),
    dpi=400, pil_kwargs={"quality": 95} , bbox_inches="tight")
    plt.close()

    # 5. Línea temporal
def temporal_line(df: pd.DataFrame):
    df = df.copy()
    df["año"] = pd.to_numeric(df["año"], errors="coerce")
    df = df.dropna(subset=["año"])
    if df.empty:
        print("No hay datos de año válidos")
        return

    df["año"] = df["año"].astype(int)
    df["revista"] = df["revista"].fillna("Desconocida").str.strip()
    df["revista"] = df["revista"].replace(r"\s+", " ", regex=True)

    # Agrupar revistas poco frecuentes
    top_n = 10
    top_revistas = df["revista"].value_counts().nlargest(top_n).index.tolist()
    df["revista"] = df["revista"].where(df["revista"].isin(top_revistas), "Otros")

    conteo = df.groupby(["año", "revista"]).size().reset_index(name="conteo")
    pivot = conteo.pivot(index="año", columns="revista", values="conteo").fillna(0)
    pivot = pivot.sort_index()
    pivot = pivot[pivot.sum().sort_values(ascending=False).index]  # ordenar columnas

    fig, ax = plt.subplots(figsize=(14, 7))
    pivot.plot(ax=ax, marker="o", linewidth=2)

    ax.set_xlabel("Año", fontsize=12)
    ax.set_ylabel("Cantidad de publicaciones", fontsize=12)
    ax.set_title("Publicaciones por año y revista", fontsize=14)
    ax.legend(title="Revista", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=9)
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    fig.savefig(
        os.path.join(settings.BASE_DIR, "mi_app/static/mi_app/imagenes/linea_temporal.png"),
        dpi=400,bbox_inches="tight")
    plt.close(fig)



# 6. Exportar a PDF
def export():
    #BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
    #ruta = os.path.join(BASE_DIR, 'resources', 'downloads')
    
    with PdfPages(os.path.join(settings.BASE_DIR, "mi_app/static/mi_app/imagenes/visualizaciones.pdf")) as pdf:
        for img in [os.path.join(settings.BASE_DIR, "mi_app/static/mi_app/imagenes/mapa_de_calor.jpg"),
        os.path.join(settings.BASE_DIR, "mi_app/static/mi_app/imagenes/nube_de_palabras.jpg"),
        os.path.join(settings.BASE_DIR, "mi_app/static/mi_app/imagenes/linea_temporal.png")]:
            fig = plt.figure()
            img_data = plt.imread(img)
            plt.imshow(img_data)
            plt.axis("off")
            pdf.savefig(fig, dpi=500,bbox_inches="tight")
            plt.close()

    print("PDF generado: visualizaciones.pdf")
