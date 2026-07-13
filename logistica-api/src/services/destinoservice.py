class DestinoService:
    def __init__(self):
        self.lista_destinos = []
    
    def registro_destino(self, destino):
        self.lista_destinos.append(destino)
        return destino
	
    def buscar_destino (self, id_destino):
        for destino in self.lista_destinos:
            if destino.id_destino == id_destino:
                return destino
        return None
	
    def actualizar_destino(self, id_destino, nuevo_nombre, nuevo_ciudad, nuevo_estado, nuevo_coordenadas, nuevo_responsable):
        destino = self.buscar_destino(id_destino)
        if destino:
            destino.nombre = nuevo_nombre
            destino.ciudad = nuevo_ciudad
            destino.estado = nuevo_estado
            destino.coordenadas = nuevo_coordenadas
            destino.responsable = nuevo_responsable
            return destino
        return None
		
    def eliminar_destino(self, id_destino):
        destino = self.buscar_destino(id_destino)
        if destino:
            self.lista_destinos.remove(destino)
            return destino
        return None