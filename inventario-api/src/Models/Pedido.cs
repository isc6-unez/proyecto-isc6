namespace InventarioAPI.Models
{
    // Representa un pedido de materiales que se va a procesar en picking
    // Es la entrada del proceso de picking
    public class Pedido
    {
        // Id del pedido
        public int IdPedido { get; set; }

        // Fecha de creacion
        public DateTime FechaCreacion { get; set; } = DateTime.Now;

        // Estado del pedido
        public EstadoPedido Estado { get; set; } = EstadoPedido.Pendiente;

        // Lista de materiales solicitados
        public List<PedidoItem> Items { get; set; } = new();
    }

    // Linea del pedido
    public class PedidoItem
    {
        // Identificador del detalle del pedido
        public int IdPedidoItem { get; set; }

        //Id del pedido
        public int IdPedido { get; set; }

        // Id del material solicitado
        public int IdMaterial { get; set; }

        // Cantidad solicitada para el picking
        public int Cantidad { get; set; }
    }

    // Estados del pedido
    public enum EstadoPedido
    {
        Pendiente,
        EnPicking,
        Completado,
        Cancelado
    }
}