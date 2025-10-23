import os
import re

#Función para combinar los archivs bib
def merge_bibtex_files( ):
    entries = {}  # claves por título o key
    merged_content = "" #archivo final combinado

    # Ruta relativa del losa crhivos descargados
    #relative_folder_path = os.path.join('DescargaApp', 'resources', 'Downloads')
    #folder_path = os.path.abspath(relative_folder_path)
    # Aseguramos que la carpeta exista
    #os.makedirs(os.path.dirname(folder_path), exist_ok=True)
    folder_path = f"DescargaApp/resources/Downloads"

    # Recorrer carpeta y subcarpetas
    input_files = []
    for root, _, files in os.walk(folder_path):
        for f in files:
            if f.endswith('.bib'): #solo archivos .bib
                input_files.append(os.path.join(root, f))

    #expresion regular para archivos completos
    entry_pattern = re.compile(r'@[\w]+\s*{[^@]*}', re.DOTALL)

    #leemos cada uno
    for file_path in input_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception as e:
            print(f" Error leyendo {file_path}: {e}")
            continue

        #extraemos todas las entradas
        raw_entries = entry_pattern.findall(content)
        for entry in raw_entries:
            match_key = re.search(r'@\w+\s*{\s*([^,]+),', entry)
            if match_key:
                key = match_key.group(1).strip()
                if key not in entries:
                    entries[key] = entry
                #else:
                    #print(f" Duplicado descartado: {key}")

    #combinamos todo en un solo acrhivo
    merged_content = '\n\n'.join(entries[k] for k in sorted(entries))

    # Ruta relativa del archivo final
    #relative_output_path = os.path.join('DescargaApp', 'resources', 'Downloads','archivo_combinado', 'archivo_final.bib')

    # Convertimos a ruta absoluta
    #output_file = os.path.abspath(relative_output_path)

    output_file = f"DescargaApp/resources/Downloads/archivo_combinado/archivofinal.bib"

    with open(output_file, 'w', encoding='utf-8') as f_out:
        f_out.write(merged_content)

    print(f" {len(input_files)} archivos combinados en: {output_file}")




