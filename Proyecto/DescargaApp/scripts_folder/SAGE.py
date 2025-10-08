from playwright.sync_api import sync_playwright, Page
from .login import login
import os
from .EstadoGlobal import estado_sage

# Función principal que automatiza la búsqueda y descarga de citas en formato BibTeX desde SAGE
def descargar_SAGE(query: str):
    try:
        # Define la ruta de descarga para los archivos BibTeX
        path = f'DescargaApp/resources/Downloads/SAGE/{query}/'
        
        os.makedirs(path, exist_ok=True)  # Crea la carpeta si no existe

        with sync_playwright() as p:
            # Lanza el navegador Chromium con animación lenta para mayor estabilidad visual
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                accept_downloads=True,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/117.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            print("Ruta temporal de descarga:", path)

            # Actualiza el estado global y realiza login
            estado_sage.actualizar_estado("Iniciando sesión")
            login(page)

            # Navega a la página principal de SAGE y acepta cookies si es necesario
            page.goto("https://journals-sagepub-com.crai.referencistas.com/")
            if page.is_visible("#onetrust-accept-btn-handler"):
                page.click("#onetrust-accept-btn-handler")

            # Realiza la búsqueda con el término proporcionado
            estado_sage.actualizar_estado("Buscando")
            page.goto(create_sage_search_url(0, query))
            page.wait_for_load_state("networkidle")

            # Calcula el número total de páginas de resultados
            total_pages = obtener_datos_sage(page)

            # Itera sobre cada página de resultados
            for i in range(1, total_pages + 1):
                page.goto(create_sage_search_url(i - 1, query))
                page.wait_for_load_state("networkidle")
                estado_sage.actualizar_descargados(
                    estado_sage.obtener_descargados() + obtener_cantidad_sage(page)
                )
                extract_sage_information(page, query, path, i)

            browser.close()
            estado_sage.actualizar_estado("Completado")

    except Exception as e:
        estado_sage.actualizar_estado("Error en el proceso")
        print(f"Error en descarga SAGE: {e}")

# Construye la URL de búsqueda para SAGE con paginación
def create_sage_search_url(page_number: int, query: str) -> str:
    q = query.replace(" ", "%20")  # Codifica espacios para URL
    return (f"https://journals-sagepub-com.crai.referencistas.com/action/doSearch"
            f"?AllField={q}&pageSize=100&startPage={page_number}")

# Obtiene el número total de resultados y calcula cuántas páginas se deben recorrer
def obtener_datos_sage(page: Page) -> int:
    locator = "#pb-page-content span.result__count"
    page.wait_for_selector(locator, timeout=60000)
    total_str = page.text_content(locator)
    total = int(total_str.replace(",", ""))  # Elimina comas y convierte a entero
    estado_sage.actualizar_encontrados(total)

    máximo = min(total, 1000)  # Limita a 1000 resultados por política de SAGE
    estado_sage.actualizar_prueba(máximo)
    return (máximo + 99) // 100  # Calcula número de páginas (100 resultados por página)

# Extrae la cantidad de resultados mostrados en la página actual
def obtener_cantidad_sage(page: Page) -> int:
    locator = "#pb-page-content span.result__current > span"
    page.wait_for_selector(locator, timeout=60000)
    text = page.text_content(locator)
    start, end = text.split("-")  # Ejemplo: "1-100"
    return int(end) - int(start) + 1

# Realiza la selección de resultados y descarga el archivo BibTeX
def extract_sage_information(page: Page, query: str, path: str, index: int):
    estado_sage.actualizar_estado("Obteniendo archivos")

    # 1. Selecciona todos los resultados de la página
    page.click("#action-bar-select-all")

    # 2. Espera a que el botón de exportación esté habilitado y lo activa
    export_btn = page.wait_for_selector("a.export-citation:not([disabled])", timeout=60000)
    export_btn.click()

    # 3. Configura el formato de exportación como BibTeX
    page.wait_for_selector("#exportCitation", timeout=60000)
    page.select_option("#citation-format", value="bibtex")
    page.dispatch_event("#citation-format", "change")

    # 4. Espera la descarga y guarda el archivo con nombre personalizado
    with page.expect_download() as dl_info:
        page.wait_for_selector("#exportCitation .form-buttons a", timeout=60000)
        page.click("#exportCitation .form-buttons a")
    download = dl_info.value
    download.save_as(os.path.join(path, f"archivo_{index}_{query}.bib"))