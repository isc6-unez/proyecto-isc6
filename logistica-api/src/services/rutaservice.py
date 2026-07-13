class RutaService:
    def __init__(self):
        self.lista_rutas = []
    
    def registro_ruta(self, ruta):
        self.lista_rutas.append(ruta)
        return ruta
	
    def buscar_ruta (self, id_ruta):
        for ruta in self.lista_rutas:
            if ruta.id_ruta == id_ruta:
                return ruta
        return None
	
    def actualizar_ruta(self, id_ruta, nuevo_origen, nuevo_destino, nuevo_distancia, nuevo_tiempo_estimado):
        ruta = self.buscar_ruta(id_ruta)
        if ruta:
            ruta.origen = nuevo_origen
            ruta.destino = nuevo_destino
            ruta.distancia = nuevo_distancia
            ruta.tiempo_estimado = nuevo_tiempo_estimado
            return ruta
        return None
		
    def eliminar_ruta(self, id_ruta):
        ruta = self.buscar_ruta(id_ruta)
        if ruta:
            self.lista_rutas.remove(ruta)
            return ruta
        return None