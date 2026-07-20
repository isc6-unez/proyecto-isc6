import variables_vehiculos

def mostrar_menu():
    print("\n--- SISTEMA DE GESTIÓN DE VEHÍCULOS (LOGÍSTICA) ---")
    print("1. Registrar nuevo vehículo")
    print("2. Mostrar vehículos registrados")
    print("3. Actualizar estado de un vehículo")
    print("4. Eliminar vehículo")
    print("5. Salir")

def iniciar_modulo():
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción (1-5): ")
        
        if opcion == "1":
            print("\n[Prueba] Ejecutando: Registrar nuevo vehículo...")
            # Aquí irá la función de crear más adelante
        elif opcion == "2":
            print("\n[Prueba] Ejecutando: Mostrar vehículos...")
            # Aquí irá la función de leer más adelante
        elif opcion == "3":
            print("\n[Prueba] Ejecutando: Actualizar estado...")
            # Aquí irá la función de actualizar más adelante
        elif opcion == "4":
            print("\n[Prueba] Ejecutando: Eliminar vehículo...")
            # Aquí irá la función de borrar más adelante
        elif opcion == "5":
            print("Saliendo del módulo de logística. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    iniciar_modulo()
    