using System;

namespace ModuloEntradasSalidas
{
    public class Entrada
    {
        public int IdEntrada { get; set; }
        public DateTime FechaEntrada { get; set; } = DateTime.Now;
        public int CapacidadRecibida { get; set; }
        public int IdProveedor { get; set; }
        public int IdLote { get; set; }
    }
}