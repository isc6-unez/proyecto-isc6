class ChoferService:
    def __init__(self):
        self.lista_choferes = []
    
    def registro_cliente(self, cliente):
        self.lista_clientes.append(cliente)
        return cliente
	
    def buscar_cliente (self, id_cliente):
        for cliente in self.lista_clientes:
            if cliente.id_cliente == id_cliente:
                return cliente
        return None
	
    def actualizar_cliente(self, id_cliente, nuevo_nombre, nuevo_direccion, nuevo_telefono, nuevo_correo):
        cliente = self.buscar_cliente(id_cliente)
        if cliente:
            cliente.nombre = nuevo_nombre
            cliente.direccion = nuevo_direccion
            cliente.telefono = nuevo_telefono
            cliente.correo = nuevo_correo
            return cliente
        return None
		
    def eliminar_cliente(self, id_cliente):
        cliente = self.buscar_cliente(id_cliente)
        if cliente:
            self.lista_clientes.remove(cliente)
            return cliente
        return None