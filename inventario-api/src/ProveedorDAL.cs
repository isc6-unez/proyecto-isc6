using System;
using System.Collections.Generic;
using System.Data;
using Npgsql;
using InventarioAPI.Models;

namespace InventarioAPI
{
    public class ProveedorDAL
    {
        private readonly string _cadenaConexion;

        public ProveedorDAL()
        {
            _cadenaConexion = "Host=100.107.111.1;Port=5432;Database=sistema_industrial;Username=dda_user;Password=EZtbuoat4;SearchPath=dda";
        }

        /// <summary>
        /// Obtiene todos los proveedores desde el servidor PostgreSQL.
        /// </summary>
        public List<Proveedor> ObtenerTodos()
        {
            List<Proveedor> lista = new List<Proveedor>();

            using (NpgsqlConnection con = new NpgsqlConnection(_cadenaConexion))
            {
                string query = "SELECT id_proveedor, rfc, nombre, nombre_empresa, telefono, email, direccion, estado FROM dda.proveedor";
                
                using (NpgsqlCommand cmd = new NpgsqlCommand(query, con))
                {
                    con.Open();
                    using (NpgsqlDataReader dr = cmd.ExecuteReader())
                    {
                        while (dr.Read())
                        {
                            lista.Add(new Proveedor
                            {
                                Id = Convert.ToInt32(dr["id_proveedor"]),
                                RfcNit = dr["rfc"] != DBNull.Value ? dr["rfc"].ToString() : string.Empty,
                                Contacto = dr["nombre"] != DBNull.Value ? dr["nombre"].ToString() : string.Empty,
                                RazonSocial = dr["nombre_empresa"] != DBNull.Value ? dr["nombre_empresa"].ToString() : string.Empty,
                                Telefono = dr["telefono"] != DBNull.Value ? dr["telefono"].ToString() : string.Empty,
                                Email = dr["email"] != DBNull.Value ? dr["email"].ToString() : string.Empty,
                                Direccion = dr["direccion"] != DBNull.Value ? dr["direccion"].ToString() : string.Empty,
                                Activo = dr["estado"] != DBNull.Value && dr["estado"].ToString().ToLower() == "activo"
                            });
                        }
                    }
                }
            }
            return lista;
        }

        /// <summary>
        /// Registra un nuevo proveedor en la base de datos.
        /// </summary>
        public bool Insertar(Proveedor p)
        {
            using (NpgsqlConnection con = new NpgsqlConnection(_cadenaConexion))
            {
                string query = @"INSERT INTO dda.proveedor (rfc, nombre, nombre_empresa, telefono, email, direccion, estado) 
                                 VALUES (@Rfc, @Nombre, @NombreEmpresa, @Telefono, @Email, @Direccion, 'Activo')";

                using (NpgsqlCommand cmd = new NpgsqlCommand(query, con))
                {
                    cmd.Parameters.AddWithValue("@Rfc", p.RfcNit ?? (object)DBNull.Value);
                    cmd.Parameters.AddWithValue("@Nombre", p.Contacto ?? (object)DBNull.Value);
                    cmd.Parameters.AddWithValue("@NombreEmpresa", p.RazonSocial ?? (object)DBNull.Value);
                    cmd.Parameters.AddWithValue("@Telefono", p.Telefono ?? (object)DBNull.Value);
                    cmd.Parameters.AddWithValue("@Email", p.Email ?? (object)DBNull.Value);
                    cmd.Parameters.AddWithValue("@Direccion", p.Direccion ?? (object)DBNull.Value);

                    con.Open();
                    return cmd.ExecuteNonQuery() > 0;
                }
            }
        }

        /// <summary>
        /// Actualiza la información de un proveedor existente.
        /// </summary>
        public bool Actualizar(Proveedor p)
        {
            using (NpgsqlConnection con = new NpgsqlConnection(_cadenaConexion))
            {
                string query = @"UPDATE dda.proveedor 
                                SET rfc = @Rfc, 
                                    nombre = @Nombre, 
                                    nombre_empresa = @NombreEmpresa, 
                                    telefono = @Telefono, 
                                    email = @Email, 
                                    direccion = @Direccion 
                                WHERE id_proveedor = @Id";

                using (NpgsqlCommand cmd = new NpgsqlCommand(query, con))
                {
                    cmd.Parameters.AddWithValue("@Id", p.Id);
                    cmd.Parameters.AddWithValue("@Rfc", p.RfcNit ?? (object)DBNull.Value);
                    cmd.Parameters.AddWithValue("@Nombre", p.Contacto ?? (object)DBNull.Value);
                    cmd.Parameters.AddWithValue("@NombreEmpresa", p.RazonSocial ?? (object)DBNull.Value);
                    cmd.Parameters.AddWithValue("@Telefono", p.Telefono ?? (object)DBNull.Value);
                    cmd.Parameters.AddWithValue("@Email", p.Email ?? (object)DBNull.Value);
                    cmd.Parameters.AddWithValue("@Direccion", p.Direccion ?? (object)DBNull.Value);

                    con.Open();
                    return cmd.ExecuteNonQuery() > 0;
                }
            }
        }

        /// <summary>
        /// Elimina un proveedor físicamente o cambia su estado.
        /// </summary>
        public bool Eliminar(int id)
        {
            using (NpgsqlConnection con = new NpgsqlConnection(_cadenaConexion))
            {
                string query = "DELETE FROM dda.proveedor WHERE id_proveedor = @Id";
                
                using (NpgsqlCommand cmd = new NpgsqlCommand(query, con))
                {
                    cmd.Parameters.AddWithValue("@Id", id);

                    con.Open();
                    return cmd.ExecuteNonQuery() > 0;
                }
            }
        }
    }
}