using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using InventarioAPI.Data;
using InventarioAPI.Models;

namespace InventarioAPI.Controllers
{
    // Ruta base del endpoint -> /api/Materiales
    [Route("api/[controller]")]
    [ApiController]
    public class MaterialesController : ControllerBase
    {
        // Conexión/Contexto privado de Entity Framework
        private readonly InventarioDbContext _context;

        // Inyección de dependencias para recibir la conexión activa a la BD
        public MaterialesController(InventarioDbContext context)
        {
            _context = context;
        }

        // 1. GET: api/Materiales (Obtiene todos los materiales registrados)
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Material>>> GetMateriales()
        {
            // Ejecuta "SELECT * FROM dda.materiales" en PostgreSQL
            return await _context.Materiales.ToListAsync();
        }

        // 2. GET: (Obtiene un material especifico por su idMaterial)
        [HttpGet("{id}")]
        public async Task<ActionResult<Material>> GetMaterial(int id)
        {
            // Busca por ID de la entidad
            var material = await _context.Materiales.FindAsync(id);

            // Si no existe el registro en la BD
            if (material == null)
            {
                return NotFound(); // Código HTTP 404
            }

            // Regresa el objeto encontrado
            return material;
        }

        // 3. POST: api/Materiales (Crea un nuevo material en la BD)
        [HttpPost]
        public async Task<ActionResult<Material>> PostMaterial(Material material)
        {
            // Prepara el objeto en la memoria del DbContext
            _context.Materiales.Add(material);
            
            // Guarda en la BD (PostgreSQL genera automaticamente el idMaterial autoincrementable)
            await _context.SaveChangesAsync();

            // Regresa código HTTP 201 Created con el ID asignado por Postgres
            return CreatedAtAction(nameof(GetMaterial), new { id = material.IdMaterial }, material);
        }

        // 4. PUT: api/Materiales/5 (Actualiza un material existente)
        [HttpPut("{id}")]
        public async Task<IActionResult> PutMaterial(int id, Material material)
        {
            // Asegura que el ID ingresado en la URL coincida con el ID del json
            if (id != material.IdMaterial)
            {
                return BadRequest("El ID de la URL no coincide con el ID del objeto enviado.");
            }

            // Le indica a Entity Framework que actualice los campos modificados
            _context.Entry(material).State = EntityState.Modified;

            try
            {
                // Guarda las modificaciones realizadas
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                // Valida si la falla fue porque el idMaterial ya no existe
                if (!MaterialExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            // Retorna HTTP 204 sin contenido
            return NoContent();
        }

        // 5. DELETE: api/Materiales/5 (Elimina un material por su ID)
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteMaterial(int id)
        {
            // Busca el material a eliminar
            var material = await _context.Materiales.FindAsync(id);
            
            // Si no existe, retorna 404
            if (material == null)
            {
                return NotFound();
            }

            // Elimina la fila de la BD
            _context.Materiales.Remove(material);
            
            // Confirma la transacción en PostgreSQL
            await _context.SaveChangesAsync();

            // Retorna HTTP 204 (No Content)
            return NoContent();
        }

        // Metodo auxiliar que valida si un idMaterial existe en la tabla
        private bool MaterialExists(int id)
        {
            return _context.Materiales.Any(e => e.IdMaterial == id);
        }
    }
}