using InventarioAPI.Models;

namespace InventarioAPI.DTOs
{
    // ---------- Material ----------
    public class MaterialCreateDto
    {
        public string Nombre { get; set; } = string.Empty;
        public string? Descripcion { get; set; }
        public int StockMinimo { get; set; }
        public string UnidadMedida { get; set; } = string.Empty;
        public int CategoriaId { get; set; }
    }

    public class MaterialUpdateDto
    {
        public string Nombre { get; set; } = string.Empty;
        public string? Descripcion { get; set; }
        public int StockMinimo { get; set; }
        public string UnidadMedida { get; set; } = string.Empty;
        public int CategoriaId { get; set; }
    }

    // ---------- Lote ----------
    public class LoteCreateDto
    {
        public string CodigoQr { get; set; } = string.Empty;
        public int CantidadInicial { get; set; }
        public DateTime? FechaFabricacion { get; set; }
        public DateTime FechaIngreso { get; set; }
        public DateTime? FechaCaducidad { get; set; }
        public string UbicacionAlmacen { get; set; } = string.Empty;
        public int IdMaterial { get; set; }
        public int IdProveedor { get; set; }
    }

    // ---------- Pedido ----------
    public class PedidoItemDto
    {
        public int IdMaterial { get; set; }
        public int Cantidad { get; set; }
    }

    public class PedidoCreateDto
    {
        public List<PedidoItemDto> Items { get; set; } = new();
    }

    // ---------- Picking ----------
    public class GenerarPickingDto
    {
        public int IdPedido { get; set; }
        public EstrategiaPicking Estrategia { get; set; } = EstrategiaPicking.FIFO;
    }
}
