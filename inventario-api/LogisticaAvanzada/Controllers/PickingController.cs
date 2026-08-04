using InventarioAPI.DTOs;
using InventarioAPI.Services;
using Microsoft.AspNetCore.Mvc;

namespace InventarioAPI.Controllers
{
    // Controlador encargado del proceso de picking del almacen.
    // El picking representa la asignacion de lotes especificos para cumplir un pedido,
    // Este controlador no descuenta inventario en la generacion, solo crea el plan.
    // El descuento real ocurre al confirmar el picking.

    [ApiController]
    [Route("api/[controller]")]
    public class PickingController : ControllerBase
    {
        private readonly IPickingService _pickingService;

        public PickingController(IPickingService pickingService)
        {
            _pickingService = pickingService;
        }

        // Genera un picking a partir de un pedido existente.
        // Calcula automaticamente los lotes a utilizar segun la estrategia seleccionada.
        // No descuenta stock en este paso.
        [HttpPost("generar")]
        public ActionResult Generar([FromBody] GenerarPickingDto dto)
        {
            var picking = _pickingService.GenerarDesdePedido(dto);

            return CreatedAtAction(
                nameof(ObtenerPorId),
                new { id = picking.IdPicking },
                picking
            );
        }

        // Retorna todos los pickings generados en el sistema.
        [HttpGet]
        public ActionResult ObtenerTodos()
        {
            return Ok(_pickingService.ObtenerTodos());
        }

        // Obtiene el detalle de un picking especifico.
        // Incluye los lotes asignados y las cantidades a retirar.
        [HttpGet("{id}")]
        public ActionResult ObtenerPorId(int id)
        {
            return Ok(_pickingService.ObtenerPorId(id));
        }

        // Confirma el picking seleccionado.
        // En este punto se descuenta el stock real de los lotes
        // y el pedido asociado pasa a estado "Completado".
        [HttpPost("{id}/confirmar")]
        public ActionResult Confirmar(int id)
        {
            var picking = _pickingService.Confirmar(id);
            return Ok(picking);
        }
    }
}