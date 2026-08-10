TRUNCATE TABLE consumo.transacciones_consumo;

INSERT INTO consumo.transacciones_consumo (
    id_transaccion,
    id_cuenta,
    id_canal,
    id_estado,
    id_sucursal,

    monto_transaccion,
    monto_calculado_items,
    diferencia_monto,

    cantidad_items,

    flag_sin_items,
    flag_inconsistencia_monto,

    fecha_transaccion,
    fecha_proceso,

    anio_transaccion,
    mes_transaccion,
    dia_transaccion,

    fecha_carga_consumo
)
SELECT
    r.id_transaccion,
    r.id_cuenta,
    r.id_canal,
    r.id_estado,
    r.id_sucursal,

    r.monto_transaccion,
    r.monto_calculado_items,
    r.diferencia_monto,

    r.cantidad_items,

    r.flag_sin_items,
    r.flag_inconsistencia_monto,

    r.fecha_transaccion,
    r.fecha_proceso,

    EXTRACT(YEAR FROM r.fecha_transaccion)::INT AS anio_transaccion,
    EXTRACT(MONTH FROM r.fecha_transaccion)::INT AS mes_transaccion,
    EXTRACT(DAY FROM r.fecha_transaccion)::INT AS dia_transaccion,

    CURRENT_TIMESTAMP AS fecha_carga_consumo
FROM refinado.transacciones_refinado r;
