using System;
using System.Collections.Generic;
using Npgsql;

namespace ModuloEntradasSalidas
{
    public class SalidaDAL
    {
        private readonly string _cadenaConexion = "Host=100.107.111.1;Port=5432;Database=sistema_industrial;Username=dda_user;Password=EZtbuoat4;SearchPath=dda";

        public List<Salida> ObtenerTodos()
        {
            List<Salida> lista = new List<Salida>();
            using (NpgsqlConnection con = new NpgsqlConnection(_cadenaConexion))
            {
                string query = "SELECT id_salida, fecha_salida, cantidad_despachada, destino, id_lote, id_proveedor FROM dda.salida";
                using (NpgsqlCommand cmd = new NpgsqlCommand(query, con))
                {
                    con.Open();
                    using (NpgsqlDataReader dr = cmd.ExecuteReader())
                    {
                        while (dr.Read())
                        {
                            lista.Add(new Salida
                            {
                                IdSalida = dr["id_salida"] != DBNull.Value ? Convert.ToInt32(dr["id_salida"]) : 0,
                                FechaSalida = dr["fecha_salida"] != DBNull.Value ? Convert.ToDateTime(dr["fecha_salida"]) : DateTime.Now,
                                CantidadDespachada = dr["cantidad_despachada"] != DBNull.Value ? Convert.ToInt32(dr["cantidad_despachada"]) : 0,
                                Destino = dr["destino"] != DBNull.Value ? dr["destino"].ToString() : string.Empty,
                                IdLote = dr["id_lote"] != DBNull.Value ? Convert.ToInt32(dr["id_lote"]) : 0,
                                IdProveedor = dr["id_proveedor"] != DBNull.Value ? Convert.ToInt32(dr["id_proveedor"]) : 0
                            });
                        }
                    }
                }
            }
            return lista;
        }

        public bool Insertar(Salida s)
        {
            using (NpgsqlConnection con = new NpgsqlConnection(_cadenaConexion))
            {
                string query = @"INSERT INTO dda.salida (fecha_salida, cantidad_despachada, destino, id_lote, id_proveedor) 
                                 VALUES (@Fecha, @Cantidad, @Destino, @IdLote, @IdProveedor)";

                using (NpgsqlCommand cmd = new NpgsqlCommand(query, con))
                {
                    cmd.Parameters.AddWithValue("@Fecha", s.FechaSalida);
                    cmd.Parameters.AddWithValue("@Cantidad", s.CantidadDespachada);
                    cmd.Parameters.AddWithValue("@Destino", s.Destino ?? (object)DBNull.Value);
                    cmd.Parameters.AddWithValue("@IdLote", s.IdLote);
                    cmd.Parameters.AddWithValue("@IdProveedor", s.IdProveedor);

                    con.Open();
                    return cmd.ExecuteNonQuery() > 0;
                }
            }
        }
    }
}