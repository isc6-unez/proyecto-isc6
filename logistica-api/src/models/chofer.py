class Chofer:
    def __init__(
        #definimos los parametros 
        self,
        id_chofer: int,
        nombre: str,
        licencia: str,
        telefono: str,
        estado: str,
        vehiculo_asignado: str
    ):
        #el de la izquierda es el parameto y el de la derecha el dato que se recibe
        self.id_chofer = id_chofer
        self.nombre = nombre
        self.licencia = licencia
        self.telefono = telefono
        self.estado = estado
        self.vehiculo_asignado = vehiculo_asignado