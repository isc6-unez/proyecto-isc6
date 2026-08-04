namespace InventarioAPI.Models
{
    // Representa el proceso de preparacion de materiales mediante picking.
    // Define qué lotes serán utilizados para completar un pedido.
    public class Picking
    {
        // Id del picking
        public int IdPicking { get; set; }

        // Pedido asociado
        public int IdPedido { get; set; }

        // Fecha de generacion
        public DateTime FechaGeneracion { get; set; } = DateTime.Now;

        // Estado del picking
        public EstadoPicking Estado { get; set; } = EstadoPicking.Generado;

        // Estrategia usada (FIFO / FEFO)
        public EstrategiaPicking Estrategia { get; set; } = EstrategiaPicking.FIFO;

        // Detalle de extraccion por lote
        public List<PickingDetalle> Detalles { get; set; } = new();
    }

    // Detalle del picking (de que lote sale el material)
    public class PickingDetalle
    {
        // Id del material
        public int IdMaterial { get; set; }

        // Id del lote
        public int IdLote { get; set; }

        // Cantidad tomada del lote
        public int CantidadTomada { get; set; }
    }

    // Estado del picking
    public enum EstadoPicking
    {
        Generado,
        Confirmado,
        Anulado
    }

    // Estrategia de seleccion de lotes
    public enum EstrategiaPicking
    {
        FIFO,
        FEFO
    }
}