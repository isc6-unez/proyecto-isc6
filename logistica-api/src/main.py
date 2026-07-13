from models.cliente import Cliente
from services.cliente_service import ClienteService

#se creo una lista vacia para almacenar los clientes
cliente_service = ClienteService()

cliente1 = Cliente(
    id_cliente=1,
    nombre="Juve Hernandez",
    correo="juvehdz05@gmail.com",
    telefono="1234321234",
    fecha_nacimiento="05/05/2005",
    direccion="EmilianoZapata"
)


cliente_service.registro_cliente(cliente1)
resultado_busqueda = cliente_service.buscar_cliente(1)
if resultado_busqueda:
    print("Cliente encontrado, con la siguiente informacion:")
    print(resultado_busqueda.nombre)  
else:
    print("Cliente no encontrado")
    # Imprime dato que se busca, en este caso el nombre del cliente con id 1

cliente_actualizado = cliente_service.actualizar_cliente(
    id_cliente=1,
    nuevo_nombre="Juve",
    nuevo_direccion="Emiliano",
    nuevo_telefono="128888888888",
    nuevo_correo="juve5@gmail.com"
)
if cliente_actualizado:
    print("CLIENTE ACTUALIZADO CORRECTAMENTE")
    print(cliente_actualizado.nombre)
    print(cliente_actualizado.direccion)
    print(cliente_actualizado.telefono)
    print(cliente_actualizado.correo)
else:
    print("Cliente no encontrado para actualizar")

cliente_eliminado = cliente_service.eliminar_cliente(1)
if cliente_eliminado:
    print("Cliente eliminado correctamente")
else:
    print("Cliente no encontrado para eliminar")

resultado_busqueda = cliente_service.buscar_cliente(1)
if resultado_busqueda:
    print("ERROOOOOR, aun existe el cliente")
else:
    print("el cliente ya no existe")