class Ruta:
    def __init__(
            self, 
            id_ruta: int,
            origen: str,
            destino: str,
            tiempo_estimado: float,
            distancia: float
    ):
        self.id_ruta = id_ruta
        self.origen = origen
        self.destino = destino
        self.tiempo_estimado = tiempo_estimado
        self.distancia = distancia
      