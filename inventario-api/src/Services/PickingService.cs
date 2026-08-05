using InventarioAPI.Data;
using InventarioAPI.DTOs;
using InventarioAPI.Models;
using InventarioAPI.Exceptions;

namespace InventarioAPI.Services
{
    
    // Servicio principal del sistema de InventarioAPI.
    // Encargado de generar y confirmar pickings a partir de pedidos.
    // Implementa la logica central del almacen:
    // - FIFO (First In, First Out)
    // - FEFO (First Expired, First Out)
    // - Control de stock por lotes
    // - Validacion de inventario disponible
    // - Confirmacion segura del descuento de stock
    // Representa el nucleo del sistema de inventario.

    public interface IPickingService
    {
        Picking GenerarDesdePedido(GenerarPickingDto dto);
        Picking Confirmar(Picking picking);
        List<Picking> ObtenerTodos();
        Picking ObtenerPorId(int id);
        Picking Confirmar(int id);

    }
    public class PickingService : IPickingService
    {
        private readonly InventarioDbContext _context;
        private readonly IPedidoService _pedidoService;
        private readonly ILoteService _loteService;

        private static List<Picking> _pickings = new();

        public PickingService(InventarioDbContext context, IPedidoService pedidoService, ILoteService loteService)
        {
            _context = context;
            _pedidoService = pedidoService;
            _loteService = loteService;
    }

        // Genera un picking a partir de un pedido.
        // No modifica el inventario, solo calcula la asignacion de lotes.
        // El pedido pasa a estado "EnPicking".
        public Picking GenerarDesdePedido(GenerarPickingDto dto)
        {
            {
                var pedido = _pedidoService.ObtenerPorId(dto.IdPedido);

                if (pedido.Estado != EstadoPedido.Pendiente)
                    throw new OperacionInvalidaException(
                        "El pedido debe estar en estado 'Pendiente' para generar picking.");

                var detalles = new List<PickingDetalle>();

                foreach (var item in pedido.Items)
                {
                    var detallesMaterial = AsignarLotesParaItem(item, dto.Estrategia);
                    detalles.AddRange(detallesMaterial);
                }

                var picking = new Picking
                {
                    IdPedido = pedido.IdPedido,
                    FechaGeneracion = DateTime.Now,
                    Estado = EstadoPicking.Generado,
                    Estrategia = dto.Estrategia,
                    Detalles = detalles
                };

                picking.IdPicking = _pickings.Count + 1;

                _pickings.Add(picking);

                pedido.Estado = EstadoPedido.EnPicking;

                return picking;
            }
        }

        // Algoritmo que asigna lotes al material especifico del pedido.
        // Aplica FIFO o FEFO y distribuye cantidades entre varios lotes si es necesario.
        private List<PickingDetalle> AsignarLotesParaItem(PedidoItem item, EstrategiaPicking estrategia)
        {
            var lotesDisponibles = _loteService.ObtenerPorMaterial(item.IdMaterial)
                .Where(l => l.EstaDisponible())
                .ToList();
                
            // Ordenamiento segun estrategia seleccionada
            if (estrategia == EstrategiaPicking.FEFO)
            {
                lotesDisponibles = lotesDisponibles
                .OrderBy(l => l.FechaCaducidad ?? DateTime.MaxValue)
                .ToList();
            }
            else
            {
                lotesDisponibles = lotesDisponibles
                .OrderBy(l => l.FechaIngreso)
                .ToList();
            }

            var stockTotal = lotesDisponibles.Sum(l => l.CantidadActual);

            if (stockTotal < item.Cantidad)
                throw new StockInsuficienteException(item.IdMaterial, item.Cantidad, stockTotal);

            var detalles = new List<PickingDetalle>();
            var cantidadPendiente = item.Cantidad;

            foreach (var lote in lotesDisponibles)
            {
                if (cantidadPendiente <= 0)
                    break;

                var cantidadATomar = Math.Min(lote.CantidadActual, cantidadPendiente);

                detalles.Add(new PickingDetalle
                {
                    IdMaterial = item.IdMaterial,
                    IdLote = lote.IdLote,
                    CantidadTomada = cantidadATomar
                });

                cantidadPendiente -= cantidadATomar;
            }

            return detalles;
        }

        // Retorna todos los pickings registrados en el sistema
        public List<Picking> ObtenerTodos()
        {
            return _pickings;
        }

        // Busca un picking por su ID
        // Lanza excepcion si no existe
        public Picking ObtenerPorId(int id)
        {
            var picking = _pickings.FirstOrDefault(p => p.IdPicking == id);

            if (picking is null)
                throw new EntidadNoEncontradaException("Picking", id);

        return picking;
        }

        // Confirma un picking utilizando su ID
        public Picking Confirmar(int id)
        {
            var picking = ObtenerPorId(id);
            return Confirmar(picking);
        }

        // Confirma un picking:
        // - Valida que el stock siga siendo valido
        // - Descuenta inventario de los lotes
        // - Cambia estado del pedido a "Completado"
        public Picking Confirmar(Picking picking)
        {
            {
                if (picking.Estado != EstadoPicking.Generado)
                    throw new OperacionInvalidaException(
                        "Solo se pueden confirmar pickings en estado 'Generado'.");

                foreach (var detalle in picking.Detalles)
                {
                    var lote = _loteService.ObtenerPorId(detalle.IdLote);

                    if (lote.CantidadActual < detalle.CantidadTomada)
                        throw new StockInsuficienteException(
                            detalle.IdMaterial,
                            detalle.CantidadTomada,
                            lote.CantidadActual);
                }

                foreach (var detalle in picking.Detalles)
                {
                    var lote = _loteService.ObtenerPorId(detalle.IdLote);
                    lote.CantidadActual -= detalle.CantidadTomada;

                    var material = _context.Materiales.Find(detalle.IdMaterial);
                    if (material == null)
                        throw new EntidadNoEncontradaException("Material", detalle.IdMaterial);
                    material.StockActual -= detalle.CantidadTomada;
                }

                picking.Estado = EstadoPicking.Confirmado;

                var pedido = _pedidoService.ObtenerPorId(picking.IdPedido);
                pedido.Estado = EstadoPedido.Completado;

                _context.SaveChanges();

                return picking;
            }
        }
    }
}