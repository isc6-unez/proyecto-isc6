// Importa las herramientas de ASP.NET Core para crear controladores API (atributos como [ApiController], [HttpGet], etc.)
using Microsoft.AspNetCore.Mvc;
// Importa Entity Framework Core para interactuar con la base de dato
using Microsoft.EntityFrameworkCore;
// Importa la clase InventarioDbContext que contiene la conexión y configuración de las tablas
using InventarioAPI.Data;
// Importa las clases de los modelos (en este caso, Categoria)
using InventarioAPI.Models;
// Define el espacio de nombres (namespace) que agrupa y organiza este controlador dentro del proyecto
namespace InventarioAPI.Controllers
{
    // Define la ruta base HTTP. [controller] se reemplaza automáticamente por "Categorias" -> /api/Categorias
    [Route("api/[controller]")]
    
    // Le indica a ASP.NET Core que esta clase es un controlador Web API (activa validaciones automáticas de JSON)
    [ApiController]
    
    // Define la clase del controlador herencia de ControllerBase (clase base para APIs sin vistas HTML)
    public class CategoriasController : ControllerBase
    {
        // Variable privada de solo lectura para almacenar la instancia del contexto de la base de datos
        private readonly InventarioDbContext _context;

        // Constructor: Inyecta la dependencia del DbContext cuando el servidor recibe una petición
        public CategoriasController(InventarioDbContext context)
        {
            // Asigna la instancia recibida a nuestra variable local privada
            _context = context;
        }


        // 1.para obtener todas las categorias  (GET)
        
        // Indica que este método responde a peticiones HTTP GET en /api/Categorias
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Categoria>>> GetCategorias()
        {
            // Consulta la tabla Categorias en PostgreSQL de forma asíncrona y regresa la lista completa
            return await _context.Categorias.ToListAsync();
        }

        // 2.para poder obtener una categoria por ID(GET por ID)
        
        // Responde a peticiones GET agregando un parámetro en la URL, por ejemplo: /api/Categorias/5
        [HttpGet("{id}")]
        public async Task<ActionResult<Categoria>> GetCategoria(int id)
        {
            // Busca la categoría por su llave primaria (id) en PostgreSQL
            var categoria = await _context.Categorias.FindAsync(id);

            // Si no encuentra ningún registro con ese ID en la BD...
            if (categoria == null)
            {
                // Retorna un código HTTP 404 (Not Found)
                return NotFound();
            }

            // Si la encuentra, retorna el objeto categoría con un código HTTP 200 (OK)
            return categoria;
        }

        // 3.para crear una nueva categoria (post)
        
        // Responde a peticiones HTTP POST en /api/Categorias (recibe los datos en el cuerpo/body del JSON)
        [HttpPost]
        public async Task<ActionResult<Categoria>> PostCategoria(Categoria categoria)
        {
            // Marca el nuevo objeto categoría para ser rastreado e insertado en el contexto
            _context.Categorias.Add(categoria);
            
            // Ejecuta el comando INSERT INTO en PostgreSQL de forma asíncrona
            await _context.SaveChangesAsync();

            // Retorna un HTTP 201 (Created), incluye la cabecera Location hacia el GET/id y devuelve la categoría guardada
            return CreatedAtAction(nameof(GetCategoria), new { id = categoria.IdCategoria }, categoria);
        }


        // 4. para actualizar una categoria existente (put)
        
        // Responde a peticiones HTTP PUT especificando el ID a editar: /api/Categorias/5
        [HttpPut("{id}")]
        public async Task<IActionResult> PutCategoria(int id, Categoria categoria)
        {
            // Valida que el ID enviado en la URL coincida con el ID dentro del objeto JSON
            if (id != categoria.IdCategoria)
            {
                // Si no coinciden, retorna un código HTTP 400 (Bad Request) con un mensaje de error
                return BadRequest("El ID de la URL no coincide con el ID del objeto enviado.");
            }

            // Marca la entidad completa como 'Modificada' para que Entity Framework sepa que debe hacer un UPDATE
            _context.Entry(categoria).State = EntityState.Modified;

            try
            {
                // Ejecuta el comando UPDATE en PostgreSQL
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException) // Captura errores de concurrencia (si alguien la borró mientras editabas)
            {
                // Verifica si la categoria realmente dejo de existir en la base de datos
                if (!CategoriaExists(id))
                {
                    // Si ya no existe, retorna un 404 (Not Found)
                    return NotFound();
                }
                else
                {
                    // Si fue otro tipo de error de concurrencia, relanza la excepción
                    throw;
                }
            }

            // Retorna un HTTP 204 (No Content), indicando que la actualización fue exitosa y no hay cuerpo que responder
            return NoContent();
        }

        // 5.para eliminar una categoria (delete)
        
        // Responde a peticiones HTTP DELETE recibiendo el ID a borrar: /api/Categorias/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteCategoria(int id)
        {
            // Busca en la base de datos la categoría que se desea eliminar
            var categoria = await _context.Categorias.FindAsync(id);
            
            // Si no existe, no se puede borrar
            if (categoria == null)
            {
                // Retorna un HTTP 404 (Not Found)
                return NotFound();
            }

            // Marca el registro encontrado para ser removido de la tabla
            _context.Categorias.Remove(categoria);
            
            // Ejecuta el comando DELETE FROM en PostgreSQL
            await _context.SaveChangesAsync();

            // Retorna un HTTP 204 (No Content) confirmando la eliminación
            return NoContent();
        }

        // metodo auxiliar de verificación
        
        // metodo privado que retorna 'true' si el ID existe en la tabla Categorias o 'false' si no
        private bool CategoriaExists(int id)
        {
            // Genera la consulta SQL de existencia (EXISTS) en PostgreSQL
            return _context.Categorias.Any(e => e.IdCategoria == id);
        }
    }
}