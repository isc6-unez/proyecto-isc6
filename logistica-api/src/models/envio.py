class Envio:
    def __init__(
        self,
        id_envio: int,
        guia: str,
        cliente: str,
        ruta: int,
        vehiculo: str,
        chofer: str,
        destino: str,
        peso: float,
        fecha_envio: str,
        estado: str
    ): 
        
        self.id_envio = id_envio
        self.guia = guia
        self.cliente = cliente
        self.ruta = ruta
        self.vehiculo = vehiculo
        self.chofer = chofer
        self.destino = destino
        self.peso = peso
        self.fecha_envio = fecha_envio
        self.estado = estado