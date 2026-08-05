using InventarioAPI.DTOs;
using InventarioAPI.Services;
using Microsoft.AspNetCore.Mvc;

namespace InventarioAPI.Controllers
{
    // Controlador encargado de la gestion de pedidos del sistema.
    //
    // Un pedido representa la solicitud de materiales realizada por un cliente.
    // Esta compuesto por una lista de items (Material + cantidad).
    //
    // Este controlador solo maneja la creacion y consulta de pedidos.
    // La asignacion de inventario y lotes se realiza posteriormente en el modulo de picking.

    [ApiController]
    [Route("api/[controller]")]
    public class PedidosController : ControllerBase
    {
        private readonly IPedidoService _pedidoService;

        public PedidosController(IPedidoService pedidoService)
        {
            _pedidoService = pedidoService;
        }

        // Crea un nuevo pedido en estado inicial "Pendiente".
        // Valida que los materiales existan y que las cantidades sean validas.
        [HttpPost]
        public ActionResult Crear([FromBody] PedidoCreateDto dto)
        {
            var pedido = _pedidoService.Crear(dto);

            return CreatedAtAction(
                nameof(ObtenerPorId),
                new { id = pedido.IdPedido },
                pedido
            );
        }

        // Retorna la lista completa de pedidos registrados en el sistema.
        [HttpGet]
        public ActionResult ObtenerTodos()
        {
            return Ok(_pedidoService.ObtenerTodos());
        }

        // Obtiene un pedido especifico por su ID.
        // Incluye la lista de items solicitados.
        [HttpGet("{id}")]
        public ActionResult ObtenerPorId(int id)
        {
            return Ok(_pedidoService.ObtenerPorId(id));
        }
    }
}