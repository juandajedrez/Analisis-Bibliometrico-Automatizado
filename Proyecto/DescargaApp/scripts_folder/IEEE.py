# Importa las herramientas necesarias de Playwright para automatización web en modo síncrono
# Importa el módulo para manipular rutas y carpetas
import os

from playwright.sync_api import Page, expect, sync_playwright

# Importa el módulo para actualizar el estado global del proceso
from .EstadoGlobal import estado_ieee
# Importa la función de login institucional desde un módulo local
from .login import login


# Función principal que gestiona todo el flujo de búsqueda y descarga de citas BibTeX desde IEEE
def descargar_IEEE(query: str):
    try:
        # Define la ruta donde se guardarán las descargas, usando el término de búsqueda como subcarpeta
        path = f"DescargaApp/resources/Downloads/IEEE/{query}/"

        # Crea la carpeta si no existe
        os.makedirs(path, exist_ok=True)

        # Inicia Playwright en modo síncrono
        with sync_playwright() as p:
            
            # Lanza el navegador Chromium en modo headless (sin interfaz gráfica)
            browser = p.chromium.launch(headless=True)

            # Crea un contexto de navegador que permite descargas y simula un navegador real con user-agent
            context = browser.new_context(
                accept_downloads=True,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/117.0.0.0 Safari/537.36",
            )

            # Abre una nueva pestaña
            page = context.new_page()
            print("Ruta temporal de descarga:", path)

            # Actualiza el estado del proceso
            estado_ieee.actualizar_estado("Iniciando sesion")

            # Realiza el login institucional usando Google
            login(page)
            # Navega a la primera página de resultados de búsqueda
            estado_ieee.actualizar_estado("Buscando")
            page.goto(create_ieee_search_url(1, query))

            # Obtiene el número total de páginas a procesar
            max = obtenerDatos(page)

            # Itera sobre cada página de resultados
            for i in range(1, max):
                page.goto(create_ieee_search_url(i, query))
                estado_ieee.actualizar_descargados(obtenerCant(page))
                extract_ieee_information(page, query, path, i)

            # Cierra el navegador al finalizar
            browser.close()
            estado_ieee.actualizar_estado("Completado")

    # Captura cualquier error que ocurra durante el proceso
    except Exception as e:
        estado_ieee.actualizar_estado("Error en el proceso ")
        print(f"Error en descarga IEEE: {e}")


# Genera una URL de búsqueda en IEEE con el término codificado y número de página
def create_ieee_search_url(page_number: int, query: str):
    query_encoded = query.replace(" ", "%20")  # Codifica espacios
    return f"https://ieeexplore-ieee-org.crai.referencistas.com/search/searchresult.jsp?newsearch=true&queryText={query_encoded}&highlight=true&returnFacets=ALL&returnType=SEARCH&matchPubs=true&rowsPerPage=100&pageNumber={page_number}"


# Extrae las citas BibTeX desde una página de resultados en IEEE
def extract_ieee_information(page: Page, query: str, path: str, i: int):
    # Selecciona todos los resultados marcando el checkbox
    page.wait_for_selector('label > input[type="checkbox"]', timeout=60000)
    page.click(
        "#xplMainContent > div.ng-SearchResults.row.g-0 > div.col > xpl-results-list > div.results-actions.hide-mobile > label > input"
    )

    estado_ieee.actualizar_estado("Obteniendo archivos")

    # Abre el menú de exportación
    page.wait_for_selector("xpl-export-search-results > button", timeout=60000)
    page.click(
        "#xplMainContent > div.ng-Dashboard > div.col-12.action-bar.hide-mobile > ul > li.Menu-item.inline-flexed.export-filter.no-line-break.pe-3.myproject-export > xpl-export-search-results > button"
    )

    # Selecciona el formato BibTeX en el modal
    page.wait_for_selector(
        "body > ngb-modal-window ul > li:nth-child(2)", timeout=60000
    )
    page.click(
        "body > ngb-modal-window > div > div > div.d-flex.align-items-center.border-bottom > ul > li:nth-child(2)"
    )

    # Marca el checkbox de BibTeX
    page.wait_for_selector('label[for="download-bibtex"] > input', timeout=60000)
    page.click('label[for="download-bibtex"] > input')

    # Espera al botón de descarga y lo activa
    page.wait_for_selector(
        "button.stats-SearchResults_Citation_Download.xpl-btn-primary", timeout=60000
    )
    with page.expect_download() as download_info:
        page.click("button.stats-SearchResults_Citation_Download.xpl-btn-primary")

    # Guarda el archivo descargado en la carpeta correspondiente
    download = download_info.value
    download.save_as(os.path.join(path, f"archivo_{i}_{query}.bib"))


# Obtiene la cantidad de resultados en la página actual
def obtenerCant(page):
    page.wait_for_selector(
        "#xplMainContent > div.ng-Dashboard > div.col > xpl-search-dashboard > section > div > h1 > span:nth-child(1) > span:nth-child(1)",
        timeout=60000,
    )
    dato = page.text_content(
        "#xplMainContent > div.ng-Dashboard > div.col > xpl-search-dashboard > section > div > h1 > span:nth-child(1) > span:nth-child(1)"
    )
    dato = int(
        (dato + "").split("-")[1].replace(",", "")
    )  # Extrae el número final del rango

    return dato


# Obtiene el número total de resultados y calcula cuántas páginas se deben procesar
def obtenerDatos(page):
    page.wait_for_selector(
        "#xplMainContent > div.ng-Dashboard > div.col > xpl-search-dashboard > section > div > h1 > span:nth-child(1) > span:nth-child(2)",
        timeout=60000,
    )
    dato = page.text_content(
        "#xplMainContent > div.ng-Dashboard > div.col > xpl-search-dashboard > section > div > h1 > span:nth-child(1) > span:nth-child(2)"
    )
    dato = int((dato + "").replace(",", ""))  # Elimina comas y convierte a entero

    # Limita el número máximo de resultados a 1000
    prueba = 1000 if dato >= 1000 else dato

    estado_ieee.actualizar_encontrados(dato)
    estado_ieee.actualizar_prueba(prueba)

    # Calcula el número de páginas necesarias (100 resultados por página)
    return int((prueba / 100) + 1) if prueba % 100 == 0 else int((prueba / 100) + 2)
