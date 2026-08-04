namespace InventarioAPI.Exceptions
{
    public class EntidadNoEncontradaException : Exception
    {
        public EntidadNoEncontradaException(string entidad, int id)
            : base($"{entidad} con ID {id} no fue encontrada.")
        {
        }
    }

    public class OperacionInvalidaException : Exception
    {
        public OperacionInvalidaException(string mensaje)
            : base(mensaje)
        {
        }
    }

    public class StockInsuficienteException : Exception
    {
        public StockInsuficienteException(int IdMaterial, decimal solicitado, decimal disponible)
            : base($"Stock insuficiente para el material {IdMaterial}. Solicitado: {solicitado}, Disponible: {disponible}")
        {
        }
    }
}