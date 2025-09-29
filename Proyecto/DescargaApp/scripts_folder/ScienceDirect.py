# Importa las herramientas necesarias de Playwright para automatización web
from playwright.sync_api import sync_playwright, Page, expect
# Importa la función de login desde el módulo local
from .login import login
# Importa el módulo para manipular rutas y carpetas
import os
# Importar la función para actualizar el estado
from .EstadoGlobal import estado_science
# Fallback HTTP fetch
import requests

def descargar_ScienceDirect(query: str):
    try:
        path = f'DescargaApp/resources/Downloads/ScienceDirect/{query}/'
        os.makedirs(path, exist_ok=True)

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                args=["--disable-blink-features=AutomationControlled"]
            )

            context = browser.new_context(
                accept_downloads=True,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/117.0.0.0 Safari/537.36",
                extra_http_headers={"Accept-Language": "en-US,en;q=0.9", "Accept": "text/html,application/xhtml+xml"},
                bypass_csp=True,
                ignore_https_errors=True
            )

            # logging de recursos fallidos / respuestas >= 400
            def on_response(resp):
                if resp.status >= 400:
                    print("RESPONSE ERROR", resp.status, resp.url)
            def on_request_failed(req):
                print("REQUEST FAILED", req.failure, req.url)

            # handler que intenta route.fetch(), si falla hace requests.get() como fallback
            def handle_route(route, request):
                try:
                    resp = route.fetch()
                    status = resp.status
                    body = resp.body()
                    headers = dict(resp.headers)
                    if status >= 400 or not body:
                        raise Exception("fetch returned error status")
                except Exception:
                    try:
                        # fallback con requests (evita bloqueos CORS del navegador)
                        r = requests.get(request.url, headers={"User-Agent": context._options.get("userAgent", "")}, timeout=20, verify=False)
                        status = r.status_code
                        body = r.content
                        headers = dict(r.headers)
                    except Exception as e:
                        print("FALLBACK FETCH ERROR", request.url, e)
                        return route.continue_()

                # añade header CORS y limpia headers potencialmente problemáticos
                headers["Access-Control-Allow-Origin"] = "*"
                headers.pop("content-encoding", None)
                headers.pop("transfer-encoding", None)
                # fulfill con el body obtenido
                try:
                    route.fulfill(status=status, headers=headers, body=body)
                except Exception:
                    route.continue_()

            # registra handlers antes de cualquier navegación/login
            context.on("response", on_response)
            context.on("requestfailed", on_request_failed)

            # patrones a interceptar (añade otros dominios si los ves en consola)
            context.route("**/*sdfestaticassets-us-east-1*/*", handle_route)
            context.route("**/*sciencedirectassets.com*/*", handle_route)
            context.route("**/*bam.nr-data.net*/*", handle_route)
            context.route("**/*elsevier-*.com*/*", handle_route)

            page = context.new_page()

            print("Ruta temporal de descarga:", path)
            estado_science.actualizar_estado("Iniciando sesion")

            # Realiza el login institucional (las rutas ya están registradas)
            login(page)
            page.wait_for_load_state("networkidle", timeout=120000)
            
            estado_science.actualizar_estado("Buscando")
            page.goto(create_sciencedirect_search_url(0, query))
            max = obtenerDatos(page)
            for i in range(1, max):
                page.goto(create_sciencedirect_search_url((i - 1) * 100, query))
                estado_science.actualizar_descargados(obtenerCant(page))
                extract_sciencedirect_information(page, query, path, i)

            browser.close()
            estado_science.actualizar_estado("Completado")

    except Exception as e:
        estado_science.actualizar_estado("Error en el proceso ")
        print(f"Error en descarga ScienceDirect: {e}")



# Generate ScienceDirect search URL
def create_sciencedirect_search_url(page_number: int, query: str):
    query_encoded = query.replace(" ", "%20")
    return f"https://www-sciencedirect-com.crai.referencistas.com/search?qs={query_encoded}&show=100&offset={page_number}"


# Extrae citas BibTeX desde ScienceDirect usando Playwright
def extract_sciencedirect_information(page: Page, query: str, path: str, i: int):

    estado_science.actualizar_estado("Obteniendo archivos")
    # click en el check de seleccionar todos
    page.click("#srp-toolbar > div.grid.row.u-display-none.u-display-inline-block-from-sm > span > span.result-header-controls-container > span:nth-child(1) > div > div > label > span.checkbox-check")

    # click en el boton de exportar
    page.click("#srp-toolbar > div.grid.row.u-display-none.u-display-inline-block-from-sm > span > span.result-header-controls-container > span.header-links-container > div.ExportAllLink.result-header-action__control.u-margin-s-left > button > span > span > span")
    
    # Espera al botón de descarga BibText y lo activa
    page.wait_for_selector('button.stats-SearchResults_Citation_Download.xpl-btn-primary', timeout=60000)
    with page.expect_download() as download_info:
        page.click("body > div:nth-child(23) > div > div > div > p > div > div > button:nth-child(5) > span > span")
    download = download_info.value
    download.save_as(os.path.join(path, f"archivo_{i}_{query}.bib"))    


def obtenerCant(page):
    # Espera al elemento que contiene el texto
    page.wait_for_selector("span.download-all-link-text", timeout=60000)

    # Obtiene el texto completo: "Download 100 articles"
    texto = page.text_content("span.download-all-link-text")

    # Extrae el número usando split y limpieza
    numero = int(texto.split()[1].replace(",", ""))

    return numero


def obtenerDatos(page):
    page.wait_for_selector("span.search-body-results-text", timeout=60000)
    dato = page.text_content("span.search-body-results-text")
    dato = int((dato + "").split()[0].replace(",", ""))

    if (dato >= 1000):
        prueba = 1000
    else:
        prueba = dato

    estado_science.actualizar_encontrados(dato)
    estado_science.actualizar_prueba(prueba)
    if (prueba % 100 == 0):
        return int((prueba / 100) + 1)
    else:
        return int((prueba / 100) + 2)