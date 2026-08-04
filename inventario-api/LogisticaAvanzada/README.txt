# Integración - Logística Avanzada

## Contenido agregado

Este paquete contiene la implementación del módulo de Logística Avanzada:

* Modelos: Pedido, Picking y Lote
* DTOs
* Servicios
* Controladores
* Exceptions
* Middleware

El módulo de Logística Avanzada utiliza el contexto de datos (Data) existente del proyecto para trabajar con la información de inventario y materiales.
El módulo fue desarrollado para trabajar en conjunto con la funcionalidad existente de **Materiales**, utilizando sus modelos y controladores actuales como parte del flujo de inventario.

El archivo Data no fue modificado, por lo que se debe conservar la versión actual del proyecto.

Copiar estas carpetas al proyecto:

```text
Models/
DTOs/
Services/
Controllers/
Exceptions/
Middleware/
```

---

## Archivos modificados

Los siguientes archivos fueron modificados:

* `appsettings.json`
* `Program.cs`
* `InventarioAPI.csproj`

**No reemplazar estos archivos completos.**
Integrar únicamente los cambios realizados para evitar sobrescribir configuraciones o avances de otros integrantes.

---

## Cambios necesarios

### `appsettings.json`

Agregar la configuración necesaria para la conexión con la base de datos.

### `Program.cs`

Agregar el registro de servicios del módulo:

* Pedido
* Picking
* Lote

Además de la configuración del middleware de excepciones.

### `InventarioAPI.csproj`

Agregar las referencias o configuraciones necesarias agregadas al proyecto.
