CREATE SCHEMA IF NOT EXISTS refinado;

CREATE TABLE IF NOT EXISTS refinado.transacciones_refinado (
    id_transaccion INT NULL,
    id_cuenta INT NULL,
    id_canal INT NULL,
    id_estado INT NULL,
    id_sucursal INT NULL,

    monto_transaccion NUMERIC(12,2) NULL,
    monto_calculado_items NUMERIC(12,2) NULL,
    diferencia_monto NUMERIC(12,2) NULL,

    cantidad_items INT NULL,

    flag_sin_items INT NULL,
    flag_inconsistencia_monto INT NULL,

    fecha_transaccion TIMESTAMP NULL,
    fecha_proceso DATE NULL,

    fecha_carga_refinado TIMESTAMP NULL
);
