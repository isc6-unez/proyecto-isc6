using System;
using System.Collections.Generic;
using Npgsql;

namespace ModuloEntradasSalidas
{
    public class EntradaDAL
    {
        private readonly string _cadenaConexion = "Host=100.107.111.1;Port=5432;Database=sistema_industrial;Username=dda_user;Password=EZtbuoat4;SearchPath=dda";

        public List<Entrada> ObtenerTodos()
        {
            List<Entrada> lista = new List<Entrada>();
            using (NpgsqlConnection con = new NpgsqlConnection(_cadenaConexion))
            {
                string query = "SELECT id_entrada, fecha_entrada, capacidad_recibida, id_proveedor, id_lote FROM dda.entrada";
                using (NpgsqlCommand cmd = new NpgsqlCommand(query, con))
                {
                    con.Open();
                    using (NpgsqlDataReader dr = cmd.ExecuteReader())
                    {
                        while (dr.Read())
                        {
                            lista.Add(new Entrada
                            {
                                IdEntrada = dr["id_entrada"] != DBNull.Value ? Convert.ToInt32(dr["id_entrada"]) : 0,
                                FechaEntrada = dr["fecha_entrada"] != DBNull.Value ? Convert.ToDateTime(dr["fecha_entrada"]) : DateTime.Now,
                                CapacidadRecibida = dr["capacidad_recibida"] != DBNull.Value ? Convert.ToInt32(dr["capacidad_recibida"]) : 0,
                                IdProveedor = dr["id_proveedor"] != DBNull.Value ? Convert.ToInt32(dr["id_proveedor"]) : 0,
                                IdLote = dr["id_lote"] != DBNull.Value ? Convert.ToInt32(dr["id_lote"]) : 0
                            });
                        }
                    }
                }
            }
            return lista;
        }

        public bool Insertar(Entrada e)
        {
            using (NpgsqlConnection con = new NpgsqlConnection(_cadenaConexion))
            {
                string query = @"INSERT INTO dda.entrada (fecha_entrada, capacidad_recibida, id_proveedor, id_lote) 
                                 VALUES (@Fecha, @Capacidad, @IdProveedor, @IdLote)";

                using (NpgsqlCommand cmd = new NpgsqlCommand(query, con))
                {
                    cmd.Parameters.AddWithValue("@Fecha", e.FechaEntrada);
                    cmd.Parameters.AddWithValue("@Capacidad", e.CapacidadRecibida);
                    cmd.Parameters.AddWithValue("@IdProveedor", e.IdProveedor);
                    cmd.Parameters.AddWithValue("@IdLote", e.IdLote);

                    con.Open();
                    return cmd.ExecuteNonQuery() > 0;
                }
            }
        }
    }
}