using InventarioAPI.Data;
using InventarioAPI.DTOs;
using InventarioAPI.Models;
using InventarioAPI.Exceptions;

namespace InventarioAPI.Services
{
    // Servicio encargado de la gestion de lotes del sistema de inventario.
    //
    // Responsabilidades principales:
    // - Crear lotes asociados a materiales
    // - Consultar lotes por material o por ID
    // - Mantener la integridad del inventario
    // - Calcular stock disponible real
    //
    // Este servicio es la base del control de inventario y es utilizado
    // directamente por el PickingService para aplicar FIFO o FEFO.

    public interface ILoteService
    {
        Lote Crear(LoteCreateDto dto);
        List<Lote> ObtenerTodos();
        List<Lote> ObtenerPorMaterial(int IdMaterial);
        Lote ObtenerPorId(int id);

        // Calcula el stock disponible real de un material.
        // Solo se consideran lotes con stock > 0 .
        int StockDisponible(int IdMaterial);
    }

    public class LoteService : ILoteService
    {
        private readonly InventarioDbContext _context;

        public LoteService(InventarioDbContext context)
        {
            _context = context;
        }

        // Crea un nuevo lote validando reglas basicas de negocio.
        public Lote Crear(LoteCreateDto dto)
        {
            // Verifica que el material exista en el sistema
            var material = _context.Materiales.Find(dto.IdMaterial);
            if (material == null)
                throw new EntidadNoEncontradaException("Material", dto.IdMaterial);

            if (dto.CantidadInicial <= 0)
                throw new OperacionInvalidaException("La cantidad del lote debe ser mayor a cero.");

            var lote = new Lote
            {
                CodigoQr = dto.CodigoQr,
                CantidadActual = dto.CantidadInicial,
                CantidadInicial = dto.CantidadInicial,
                
                FechaFabricacion = dto.FechaFabricacion.HasValue
                ? DateTime.SpecifyKind(dto.FechaFabricacion.Value, DateTimeKind.Utc)
                : null,

                FechaIngreso = DateTime.SpecifyKind(dto.FechaIngreso, DateTimeKind.Utc),

                FechaCaducidad = dto.FechaCaducidad.HasValue
                ? DateTime.SpecifyKind(dto.FechaCaducidad.Value, DateTimeKind.Utc)
                : null,
                
                UbicacionAlmacen = dto.UbicacionAlmacen,
                IdMaterial = dto.IdMaterial,
                IdProveedor = dto.IdProveedor,
            };

            _context.Lotes.Add(lote);
            _context.SaveChanges();

            material.StockActual += dto.CantidadInicial;
            _context.SaveChanges();

            return lote;
        }

        // Obtiene todos los lotes del sistema
        public List<Lote> ObtenerTodos() => _context.Lotes.ToList();

        // Obtiene todos los lotes asociados a un material
        public List<Lote> ObtenerPorMaterial(int IdMaterial)
        {
            return _context.Lotes
                .Where(l => l.IdMaterial == IdMaterial)
                .ToList();
        }

        // Busca un lote por ID
        // Lanza excepcion si no existe
        public Lote ObtenerPorId(int id)
        {
            var lote = _context.Lotes.FirstOrDefault(l => l.IdLote == id);

            if (lote is null)
                throw new EntidadNoEncontradaException("Lote", id);

            return lote;
        }

        // Calcula el stock disponible real de un material.
        // Aplica la regla de negocio: solo lotes validos.
        public int StockDisponible(int IdMaterial)
        {
            return _context.Lotes
                .Where(l => l.IdMaterial == IdMaterial && l.EstaDisponible())
                .Sum(l => l.CantidadActual);
        }
    }
}