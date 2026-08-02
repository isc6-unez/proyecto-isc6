using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;


namespace InventarioAPI.Models
{
    // Representa un lote fisico dentro del almacen
    // El inventario se maneja por lotes para asegurar trazabilidad
    [Table("lote", Schema = "dda")]
    public class Lote
    {
        // Identificador del lote
        [Key]
        [Column("id_lote")]
        public int IdLote { get; set; }

        // Codigo QR unico del lote.
        [Column("codigo_qr")]
        public string CodigoQr { get; set; } = string.Empty;

        // Cantidad inicial del lote
        [Column("cantidad_inicial")]
        public int CantidadInicial { get; set; }

        // Cantidad disponible actualmente
        [Column("cantidad_actual")]
        public int CantidadActual { get; set; }

        // Fecha de fabricacion.
        [Column("fecha_fabricacion")]
        public DateTime? FechaFabricacion { get; set; }

        // Fecha de ingreso al almacen
        [Column("fecha_ingreso")]
        public DateTime FechaIngreso { get; set; }

        // Fecha de caducidad del producto
        [Column("fecha_caducidad")]
        public DateTime? FechaCaducidad { get; set; }

        // Ubicacion del lote dentro del almacen
        [Column("ubicacion_almacen")]
        public string UbicacionAlmacen { get; set; } = string.Empty;

        // material al que pertenece el lote
        [Column("id_material")]
        public int IdMaterial { get; set; }

        [ForeignKey("IdMaterial")]
        public virtual Material? Material { get; set; }

        // Id del proveedor del lote
        [Column("id_proveedor")]
        public int IdProveedor { get; set; }

        // Verifica si el lote esta disponible para picking
        public bool EstaDisponible()
        {
            return CantidadActual > 0 &&
            (!FechaCaducidad.HasValue || FechaCaducidad.Value >= DateTime.Today);
        }
    }
}