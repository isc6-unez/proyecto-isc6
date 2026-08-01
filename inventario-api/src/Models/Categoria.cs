using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace InventarioAPI.Models
{
    [Table("categoria", Schema = "dda")]
    public class Categoria
    {
        [Key]
        [Column("id_categoria")]
        public int IdCategoria { get; set; }

        [Required]
        [Column("nombre_categoria")]
        [StringLength(100)]
        public string NombreCategoria { get; set; } = string.Empty;

        [Column("descripcion")]
        public string? Descripcion { get; set; }
    }
}