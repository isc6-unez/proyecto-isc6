class Vehiculo:
    def __init__(
            self,
            id_vehiculo: int,
            placas: str,
            modelo: str,
            capacidad_maxima: float,
            tipo_vehiculo: str,
            estado: str

    ):
        self.id_vehiculo = id_vehiculo
        self.placas = placas
        self.modelo = modelo
        self.capacidad_maxima = capacidad_maxima
        self.tipo_vehiculo = tipo_vehiculo
        self.estado = estado