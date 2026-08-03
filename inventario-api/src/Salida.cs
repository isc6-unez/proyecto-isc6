using System;

namespace ModuloEntradasSalidas
{
    public class Salida
    {
        public int IdSalida { get; set; }
        public DateTime FechaSalida { get; set; } = DateTime.Now;
        public int CantidadDespachada { get; set; }
        public string Destino { get; set; } = string.Empty;
        public int IdLote { get; set; }
        public int IdProveedor { get; set; }
    }
}