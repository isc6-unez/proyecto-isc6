class Destino:
    def __init__(
            self, 
            id_destino: int,
            nombre: str,
            ciudad: str,
            estado: str,
            coordenadas: str,
            responsable: str,
    ): 
        self.id_destino = id_destino
        self.nombre = nombre
        self.ciudad = ciudad
        self.estado = estado
        self.coordenadas = coordenadas
        self.responsable = responsable