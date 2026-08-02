using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace InventarioAPI.Models
{
    [Table("material", Schema = "dda")]
    public class Material
    {
        [Key]
        [Column("id_material")]
        public int IdMaterial { get; set; }

        [Required]
        [Column("nombre")]
        [StringLength(150)]
        public string Nombre { get; set; } = string.Empty;

        [Column("descripcion")]
        public string? Descripcion { get; set; }

        [Required]
        [Column("stock_minimo")]
        public int StockMinimo { get; set; }

        [Column("stock_actual")]
        public int StockActual { get; set; } = 0;

        [Required]
        [Column("unidad_medida")]
        [StringLength(20)]
        public string UnidadMedida { get; set; } = string.Empty;

        [Required]
        [Column("id_categoria")]
        public int IdCategoria { get; set; }

        // Relación con Categoria
        [ForeignKey("IdCategoria")]
        public virtual Categoria? Categoria { get; set; }
    }
}