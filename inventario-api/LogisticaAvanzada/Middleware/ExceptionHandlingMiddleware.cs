using System.Net;
using System.Text.Json;
using InventarioAPI.Exceptions;

namespace InventarioAPI.Middleware
{
    // Middleware encargado de interceptar todas las excepciones del sistema
    // y transformarlas en respuestas HTTP controladas y consistentes.
    //
    // Su objetivo es evitar que la API devuelva errores 500 genericos
    // cuando ocurren fallos de logica de negocio.
    //
    // Convierte excepciones en respuestas JSON estructuradas con:
    // - codigo de error
    // - mensaje descriptivo
    // - status HTTP adecuado

    public class ExceptionHandlingMiddleware
    {
        private readonly RequestDelegate _next;

        public ExceptionHandlingMiddleware(RequestDelegate next)
        {
            _next = next;
        }

        // Punto de entrada del middleware en la pipeline HTTP
        public async Task InvokeAsync(HttpContext context)
        {
            try
            {
                await _next(context);
            }
            catch (StockInsuficienteException ex)
            {
                await EscribirError(context, HttpStatusCode.BadRequest, "STOCK_INSUFICIENTE", ex.Message);
            }
            catch (EntidadNoEncontradaException ex)
            {
                await EscribirError(context, HttpStatusCode.NotFound, "NO_ENCONTRADO", ex.Message);
            }
            catch (OperacionInvalidaException ex)
            {
                await EscribirError(context, HttpStatusCode.BadRequest, "OPERACION_INVALIDA", ex.Message);
            }
            catch (Exception ex)
            {
                await EscribirError(context, HttpStatusCode.InternalServerError, "ERROR_INTERNO", ex.Message);
            }
        }

        // Convierte cualquier excepcion en una respuesta JSON estructurada
        // con codigo HTTP y mensaje de error.
        private static async Task EscribirError(
            HttpContext context,
            HttpStatusCode statusCode,
            string codigo,
            string mensaje)
        {
            context.Response.ContentType = "application/json";
            context.Response.StatusCode = (int)statusCode;

            var payload = JsonSerializer.Serialize(new
            {
                codigo,
                mensaje
            });

            await context.Response.WriteAsync(payload);
        }
    }
}