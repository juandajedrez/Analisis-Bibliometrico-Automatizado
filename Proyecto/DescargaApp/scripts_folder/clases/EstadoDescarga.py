import threading

class EstadoDescarga:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self._estado = "Iniciando..."
        self._encontrados = 0
        self._descargados = 0
        self._lock = threading.Lock()
        self._prueba = 0

    def actualizar_prueba(self, prueba: int):
        with self._lock:
            self._prueba = prueba

    def actualizar_estado(self, estado: str):
        with self._lock:
            self._estado = estado

    def actualizar_encontrados(self, cantidad: int):
        with self._lock:
            self._encontrados = cantidad

    def actualizar_descargados(self, cantidad: int):
        with self._lock:
            self._descargados = cantidad

    def obtener_prueba(self):
        with self._lock:
            return self._prueba
        
    def obtener_estado(self):
        with self._lock:
            return self._estado

    def obtener_encontrados(self):
        with self._lock:
            return self._encontrados

    def obtener_descargados(self):
        with self._lock:
            return self._descargados

    def obtener_porcentaje(self):
        with self._lock:
            if self._encontrados > 0:
                return round((self._descargados / self._encontrados) * 100)
            return 0
    
    def clear(self):
        with self._lock:
            self._estado = "Iniciando..."
            self._encontrados = 0
            self._descargados = 0
            self._prueba = 0