class VehiculoService:
    def __init__(self):
        self.lista_vehiculos = []
    
    def registro_vehiculo(self, vehiculo):
        self.lista_vehiculos.append(vehiculo)
        return vehiculo
	
    def buscar_vehiculo (self, id_vehiculo):
        for vehiculo in self.lista_vehiculos:
            if vehiculo.id_vehiculo == id_vehiculo:
                return vehiculo
        return None
	
    def actualizar_vehiculo(self, id_vehiculo, nuevo_placas, nuevo_modelo, nuevo_capacidad_maxima, nuevo_tipo_vehiculo, nuevo_estado):
        vehiculo = self.buscar_vehiculo(id_vehiculo)
        if vehiculo:
            vehiculo.placas = nuevo_placas
            vehiculo.modelo = nuevo_modelo
            vehiculo.capacidad_maxima = nuevo_capacidad_maxima
            vehiculo.tipo_vehiculo = nuevo_tipo_vehiculo
            vehiculo.estado = nuevo_estado
            return vehiculo
        return None
		
    def eliminar_vehiculo(self, id_vehiculo):
        vehiculo = self.buscar_vehiculo(id_vehiculo)
        if vehiculo:
            self.lista_vehiculos.remove(vehiculo)
            return vehiculo
        return None