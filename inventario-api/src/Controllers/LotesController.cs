using InventarioAPI.DTOs;
using InventarioAPI.Services;
using Microsoft.AspNetCore.Mvc;

namespace InventarioAPI.Controllers
{
    // Controlador encargado de la gestion de lotes de inventario.
    //
    // Un lote representa una entrada fisica de un material en el almacen,
    // con cantidad, fecha de ingreso y ubicacion dentro del almacen.
    //
    // Este controlador permite registrar lotes y consultar stock real disponible.

    [ApiController]
    [Route("api/[controller]")]
    public class LotesController : ControllerBase
    {
        private readonly ILoteService _loteService;

        public LotesController(ILoteService loteService)
        {
            _loteService = loteService;
        }

        // Registra un nuevo lote en el sistema.
        // Representa la entrada de mercaderia al almacen.
        // Retorna el lote creado con su ID generado.
        [HttpPost]
        public ActionResult Crear([FromBody] LoteCreateDto dto)
        {
            var lote = _loteService.Crear(dto);

            return CreatedAtAction(
                nameof(ObtenerPorId),
                new { id = lote.IdLote },
                lote
            );
        }

        // Retorna todos los lotes existentes en el almacen.
        [HttpGet]
        public ActionResult ObtenerTodos()
        {
            return Ok(_loteService.ObtenerTodos());
        }

        // Retorna un lote especifico por su ID.
        // Si no existe, el middleware maneja la excepcion.
        [HttpGet("{id}")]
        public ActionResult ObtenerPorId(int id)
        {
            return Ok(_loteService.ObtenerPorId(id));
        }

        // Retorna todos los lotes asociados a un material especifico.
        [HttpGet("Material/{IdMaterial}")]
        public ActionResult ObtenerPorMaterial(int IdMaterial)
        {
            return Ok(_loteService.ObtenerPorMaterial(IdMaterial));
        }

        // Consulta el stock disponible de un material.
        // Solo considera lotes con cantidad disponible mayor a cero.
        // Retorna un objeto estructurado con el resultado.
        [HttpGet("Material/{IdMaterial}/stock")]
        public ActionResult StockDisponible(int IdMaterial)
        {
            var stock = _loteService.StockDisponible(IdMaterial);

            return Ok(new
            {
                IdMaterial = IdMaterial,
                StockDisponible = stock
            });
        }
    }
}