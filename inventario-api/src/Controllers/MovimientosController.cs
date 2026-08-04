using Microsoft.AspNetCore.Mvc;
using Npgsql;

namespace InventarioAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class MovimientosController : ControllerBase
    {
        private readonly string _connectionString;

        public MovimientosController(IConfiguration configuration)
        {
            // Lee la conexión que agregaste en appsettings.json
            _connectionString = configuration.GetConnectionString("DefaultConnection")!;
        }

        [HttpGet]
        public async Task<IActionResult> Get()
        {
            var movimientos = new List<Dictionary<string, object>>();

            try
            {
                await using var conn = new NpgsqlConnection(_connectionString);
                await conn.OpenAsync();

                // Consulta a la tabla dda.movimiento_inventario
                await using var cmd = new NpgsqlCommand("SELECT * FROM dda.material;", conn);
                await using var reader = await cmd.ExecuteReaderAsync();

                while (await reader.ReadAsync())
                {
                    var fila = new Dictionary<string, object>();
                    for (int i = 0; i < reader.FieldCount; i++)
                    {
                        fila[reader.GetName(i)] = reader.IsDBNull(i) ? null! : reader.GetValue(i);
                    }
                    movimientos.Add(fila);
                }

                return Ok(movimientos);
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { 
                    error = "Error de conexión a PostgreSQL", 
                    detalle = ex.Message 
                });
            }
        }
    }
}