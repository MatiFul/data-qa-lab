USE qa_lab_v3;

DROP TABLE IF EXISTS transacciones_refinado;

CREATE TABLE transacciones_refinado (
    id_transaccion INT NULL,
    id_cuenta INT NULL,
    id_canal INT NULL,
    id_estado INT NULL,
    id_sucursal INT NULL,

    monto_transaccion DECIMAL(12,2) NULL,
    monto_calculado_items DECIMAL(12,2) NULL,
    diferencia_monto DECIMAL(12,2) NULL,

    cantidad_items INT NULL,

    flag_sin_items INT NULL,
    flag_inconsistencia_monto INT NULL,

    fecha_transaccion DATETIME NULL,
    fecha_proceso DATE NULL,

    fecha_carga_refinado DATETIME NULL
)
ENGINE=OLAP
DUPLICATE KEY(id_transaccion)
DISTRIBUTED BY HASH(id_transaccion) BUCKETS 5
PROPERTIES (
    "replication_num" = "1"
);