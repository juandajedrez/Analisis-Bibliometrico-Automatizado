from playwright.sync_api import sync_playwright, Page
from ..resources.credentials import *  # Importa las credenciales de acceso (usuario y contraseña)

# Función que automatiza el inicio de sesión en IEEE Xplore a través de IntelProxy con cuenta Google
def login(page: Page):
    # URL de acceso que redirige a la autenticación con Google vía IntelProxy
    login_url = (
        "https://login.intelproxy.com/v2/conector/google/solicitar?"+
        "cuenta=7Ah6RNpGWF22jjyq&url=ezp.2aHR0cHM6Ly9pZWVleHBsb3JlLmllZWUub3JnL3NlYXJjaC9zZWFyY2hyZXN1bHQuanNwP2FjdGlvbj1zZWFyY2gmbmV3c2VhcmNoPXRydWU-"
    )

    # Navega a la URL de login
    page.goto(login_url)

    # Completa el campo de correo electrónico con el nombre de usuario
    page.fill('input[type="email"]', username)
    page.click("#identifierNext")  # Avanza al siguiente paso

    # Espera a que aparezca el campo de contraseña
    page.wait_for_selector('input[type="password"]')

    # Completa el campo de contraseña
    page.fill('input[type="password"]', password)
    page.click("#passwordNext")  # Finaliza el login

    # Espera a que se redirija correctamente a la página de búsqueda de IEEE Xplore
    page.wait_for_url(
        "https://ieeexplore-ieee-org.crai.referencistas.com/search/searchresult.jsp?action=search&newsearch=true",
        timeout=60000  # Espera hasta 60 segundos
    )