CREATE SCHEMA IF NOT EXISTS curado;

CREATE TABLE IF NOT EXISTS curado.transacciones_curado (
    id_transaccion INT NULL,
    id_cuenta INT NULL,
    id_canal INT NULL,
    id_estado INT NULL,
    id_sucursal INT NULL,
    monto NUMERIC(12,2) NULL,
    fecha_transaccion TIMESTAMP NULL,
    fecha_proceso DATE NULL,
    fecha_carga_curado TIMESTAMP NULL
);

CREATE TABLE IF NOT EXISTS curado.items_transaccion_curado (
    id_item INT NULL,
    id_transaccion INT NULL,
    id_producto INT NULL,
    cantidad INT NULL,
    precio_unitario NUMERIC(12,2) NULL,
    fecha_carga_curado TIMESTAMP NULL
);

CREATE TABLE IF NOT EXISTS curado.clientes_curado (
    id_cliente INT NULL,
    nombre TEXT NULL,
    dni BIGINT NULL,
    email TEXT NULL,
    fecha_alta DATE NULL,
    fecha_carga_curado TIMESTAMP NULL
);

CREATE TABLE IF NOT EXISTS curado.cuentas_curado (
    id_cuenta INT NULL,
    id_cliente INT NULL,
    tipo_cuenta TEXT NULL,
    estado_cuenta TEXT NULL,
    fecha_alta DATE NULL,
    fecha_carga_curado TIMESTAMP NULL
);

CREATE TABLE IF NOT EXISTS curado.productos_curado (
    id_producto INT NULL,
    nombre_producto TEXT NULL,
    categoria TEXT NULL,
    activo INT NULL,
    fecha_carga_curado TIMESTAMP NULL
);

CREATE TABLE IF NOT EXISTS curado.canales_curado (
    id_canal INT NULL,
    descripcion_canal TEXT NULL,
    fecha_carga_curado TIMESTAMP NULL
);

CREATE TABLE IF NOT EXISTS curado.sucursales_curado (
    id_sucursal INT NULL,
    nombre_sucursal TEXT NULL,
    provincia TEXT NULL,
    fecha_carga_curado TIMESTAMP NULL
);

CREATE TABLE IF NOT EXISTS curado.estados_transaccion_curado (
    id_estado INT NULL,
    descripcion_estado TEXT NULL,
    es_final INT NULL,
    fecha_carga_curado TIMESTAMP NULL
);
