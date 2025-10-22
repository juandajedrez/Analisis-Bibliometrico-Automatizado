import os

from .scripts_folder.clustering import pipeline_from_bibtex
from .scripts_folder.visualAnalisis import data_from_bibtext

# Obtenemos la ruta base general del proeycto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))

# Ruta relativa del archivo final
relative_output_path = os.path.join('DescargaApp', 'resources', 'Downloads','archivo_combinado', 'archivo_final.bib')

# Convertimos a ruta absoluta
output_file = os.path.abspath(relative_output_path)

def generate_dendograma():

    # definimos la ruta con el bibtext y la ruta donde se guardaran los dendogramas
    #ruta = os.path.join(BASE_DIR,'mi_app', 'resources', 'downloads', 'archivofinal.bib')
    salida= os.path.join(BASE_DIR,'mi_app','static' ,'mi_app','outputs')
    os.makedirs(salida,exist_ok=True)

    return pipeline_from_bibtex(output_file,salida)

def generate_visuals():

    #rutav = os.path.join(BASE_DIR,'mi_app', 'resources', 'downloads', 'archivofinal.bib')
    data_from_bibtext(output_file)