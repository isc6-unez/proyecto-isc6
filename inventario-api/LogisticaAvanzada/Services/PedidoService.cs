using InventarioAPI.Data;
using InventarioAPI.DTOs;
using InventarioAPI.Models;
using InventarioAPI.Exceptions;

namespace InventarioAPI.Services
{
    // Servicio encargado de la gestion de pedidos.
    //
    // Un pedido representa la solicitud de uno o varios materiales con cantidades especificas.
    // Es el punto de entrada del flujo logistico:
    // Pedido → Picking → Descuento de inventario (lotes)
    //
    // Responsabilidades:
    // - Crear pedidos con validacion de materiales y cantidades
    // - Consultar pedidos existentes
    // - Obtener pedidos por ID
    //
    // No maneja inventario ni stock, solo estructura de solicitud.

    public interface IPedidoService
    {
        Pedido Crear(PedidoCreateDto dto);
        List<Pedido> ObtenerTodos();
        Pedido ObtenerPorId(int id);
    }

    public class PedidoService : IPedidoService
    {
        private readonly InventarioDbContext _context;
        private static List<Pedido> _pedidos = new();

        public PedidoService(InventarioDbContext context)
        {
            _context = context;
        }

        // Crea un nuevo pedido validando:
        // - que tenga al menos un item
        // - que los materiales existan
        // - que las cantidades sean validas (> 0)
        public Pedido Crear(PedidoCreateDto dto)
        {
            if (dto.Items is null || dto.Items.Count == 0)
                throw new OperacionInvalidaException("El pedido debe contener al menos un item.");

            // Validacion de cada material del pedido
            foreach (var item in dto.Items)
            {
                // Verifica existencia del material
                var material = _context.Materiales.Find(item.IdMaterial);
                if (material == null)
                    throw new EntidadNoEncontradaException("Material", item.IdMaterial);

                // Valida cantidad solicitada
                if (item.Cantidad <= 0)
                    throw new OperacionInvalidaException(
                        $"La cantidad de la materia prima {item.IdMaterial} debe ser mayor a cero.");
            }

            var pedido = new Pedido
            {
                FechaCreacion = DateTime.Now,
                Estado = EstadoPedido.Pendiente,
                Items = dto.Items.Select(i => new PedidoItem
                {
                    IdMaterial = i.IdMaterial,
                    Cantidad = i.Cantidad
                }).ToList()
            };

            pedido.IdPedido = _pedidos.Count + 1;
            foreach (var item in pedido.Items)
            {
                item.IdPedido = pedido.IdPedido;
                item.IdPedidoItem = pedido.Items.IndexOf(item) + 1;
            }

            _pedidos.Add(pedido);
            return pedido;
        }

        // Retorna todos los pedidos registrados en el sistema
        public List<Pedido> ObtenerTodos() => _pedidos;

        // Busca un pedido por su ID
        // Lanza excepcion si no existe
        public Pedido ObtenerPorId(int id)
        {
            var pedido = _pedidos.FirstOrDefault(p => p.IdPedido == id);

            if (pedido is null)
                throw new EntidadNoEncontradaException("Pedido", id);

            return pedido;
        }
    }
}