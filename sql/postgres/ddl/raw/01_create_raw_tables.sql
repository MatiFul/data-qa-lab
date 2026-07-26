CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.clientes_raw (
    id_cliente INT NULL,
    nombre TEXT NULL,
    dni BIGINT NULL,
    email TEXT NULL,
    fecha_alta DATE NULL
);

CREATE TABLE IF NOT EXISTS raw.cuentas_raw (
    id_cuenta INT NULL,
    id_cliente INT NULL,
    tipo_cuenta TEXT NULL,
    estado_cuenta TEXT NULL,
    fecha_alta DATE NULL
);

CREATE TABLE IF NOT EXISTS raw.productos_raw (
    id_producto INT NULL,
    nombre_producto TEXT NULL,
    categoria TEXT NULL,
    activo INT NULL
);

CREATE TABLE IF NOT EXISTS raw.estados_transaccion_raw (
    id_estado INT NULL,
    descripcion_estado TEXT NULL,
    es_final INT NULL
);

CREATE TABLE IF NOT EXISTS raw.canales_raw (
    id_canal INT NULL,
    descripcion_canal TEXT NULL
);

CREATE TABLE IF NOT EXISTS raw.sucursales_raw (
    id_sucursal INT NULL,
    nombre_sucursal TEXT NULL,
    provincia TEXT NULL
);

CREATE TABLE IF NOT EXISTS raw.transacciones_raw (
    id_transaccion INT NULL,
    id_cuenta INT NULL,
    id_canal INT NULL,
    id_estado INT NULL,
    id_sucursal INT NULL,
    monto NUMERIC(12,2) NULL,
    fecha_transaccion TIMESTAMP NULL,
    fecha_proceso DATE NULL
);

CREATE TABLE IF NOT EXISTS raw.items_transaccion_raw (
    id_item INT NULL,
    id_transaccion INT NULL,
    id_producto INT NULL,
    cantidad INT NULL,
    precio_unitario NUMERIC(12,2) NULL
);
