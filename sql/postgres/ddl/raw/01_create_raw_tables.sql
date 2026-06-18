CREATE SCHEMA IF NOT EXISTS raw;

DROP TABLE IF EXISTS raw.clientes_raw;
CREATE TABLE raw.clientes_raw (
    id_cliente INT NULL,
    nombre TEXT NULL,
    dni BIGINT NULL,
    email TEXT NULL,
    fecha_alta DATE NULL
);

DROP TABLE IF EXISTS raw.cuentas_raw;
CREATE TABLE raw.cuentas_raw (
    id_cuenta INT NULL,
    id_cliente INT NULL,
    tipo_cuenta TEXT NULL,
    estado_cuenta TEXT NULL,
    fecha_alta DATE NULL
);

DROP TABLE IF EXISTS raw.productos_raw;
CREATE TABLE raw.productos_raw (
    id_producto INT NULL,
    nombre_producto TEXT NULL,
    categoria TEXT NULL,
    activo INT NULL
);

DROP TABLE IF EXISTS raw.estados_transaccion_raw;
CREATE TABLE raw.estados_transaccion_raw (
    id_estado INT NULL,
    descripcion_estado TEXT NULL,
    es_final INT NULL
);

DROP TABLE IF EXISTS raw.canales_raw;
CREATE TABLE raw.canales_raw (
    id_canal INT NULL,
    descripcion_canal TEXT NULL
);

DROP TABLE IF EXISTS raw.sucursales_raw;
CREATE TABLE raw.sucursales_raw (
    id_sucursal INT NULL,
    nombre_sucursal TEXT NULL,
    provincia TEXT NULL
);

DROP TABLE IF EXISTS raw.transacciones_raw;
CREATE TABLE raw.transacciones_raw (
    id_transaccion INT NULL,
    id_cuenta INT NULL,
    id_canal INT NULL,
    id_estado INT NULL,
    id_sucursal INT NULL,
    monto NUMERIC(12,2) NULL,
    fecha_transaccion TIMESTAMP NULL,
    fecha_proceso DATE NULL
);

DROP TABLE IF EXISTS raw.items_transaccion_raw;
CREATE TABLE raw.items_transaccion_raw (
    id_item INT NULL,
    id_transaccion INT NULL,
    id_producto INT NULL,
    cantidad INT NULL,
    precio_unitario NUMERIC(12,2) NULL
);