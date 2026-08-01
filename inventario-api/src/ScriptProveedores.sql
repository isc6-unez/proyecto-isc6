CREATE TABLE IF NOT EXISTS dda.proveedor (
    id_proveedor SERIAL PRIMARY KEY,
    razonsocial VARCHAR(150) NOT NULL,
    rfcnit VARCHAR(20) NOT NULL,
    contacto VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion VARCHAR(250),
    activo BOOLEAN DEFAULT true
);
