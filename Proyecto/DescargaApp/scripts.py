import os
import sys
import requests
import threading

# Importa las funciones de scraping específicas para cada fuente
from .scripts_folder.IEEE import descargar_IEEE
from .scripts_folder.SAGE import descargar_SAGE

# Función principal que inicia el scraping en paralelo para IEEE y SAGE
def run(query: str):
    # Lanza dos hilos independientes para ejecutar los scrapers simultáneamente
    threading.Thread(target=descargar_IEEE, args=(query,)).start()
    threading.Thread(target=descargar_SAGE, args=(query,)).start()
    return  # No espera a que terminen los hilos; ejecución asíncrona

# Añade la raíz del proyecto al path del sistema para permitir imports compartidos
# Esto es útil cuando se necesita acceder a módulos fuera del paquete actual
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

# Importa las credenciales de acceso desde un módulo centralizado
# Esto permite mantener la autenticación separada del código de scraping
from .resources.credentials import username, password











