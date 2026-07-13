class EnvioService:
    def __init__(self):
        #se creo una lista para almacenar los envios, como si fuera una libreta vacia creada.
        self.lista_envios = []
    #Recibe los envios  
    def registro_envio(self,envio):
        #Lo que hace es agregar el envio a la lista de envios, como si fuera una libreta donde se van agregando los envios.
        self.lista_envios.append(envio)
        return envio
    
    def buscar_envio(self, guia):
        for envio in self.lista_envios:
            #compara si la guia del envio es igual a la guia que se esta buscando,
            if envio.guia == guia:
                return envio
        #no se encontro el envio con la guia especificada
        return None
    
    def actualizar_envio(self, guia, nuevo_estado):
        envio = self.buscar_envio(guia)
        if envio:
            envio.estado = nuevo_estado
            return envio
        return None
    
    def eliminar_envio(self, guia):
        envio = self.buscar_envio(guia)
        if envio:
            self.lista_envios.remove(envio)
            return envio
        return None
