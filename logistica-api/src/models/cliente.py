class Cliente:
    def __init__(
        #definimos los parametros 
        self,
        id_cliente: int,
        nombre: str,
        correo: str,
        telefono: str,
        fecha_nacimiento: str,
        direccion: str
    ):
        #el de la izquierda es el parameto y el de la derecha el dato que se recibe
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.fecha_nacimiento = fecha_nacimiento
        self.direccion = direccion