TRUNCATE TABLE refinado.transacciones_refinado;

INSERT INTO refinado.transacciones_refinado (
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

    fecha_carga_refinado
)
SELECT
    t.id_transaccion,
    t.id_cuenta,
    t.id_canal,
    t.id_estado,
    t.id_sucursal,

    t.monto AS monto_transaccion,
    COALESCE(SUM(i.cantidad * i.precio_unitario), 0) AS monto_calculado_items,
    t.monto - COALESCE(SUM(i.cantidad * i.precio_unitario), 0) AS diferencia_monto,

    COUNT(i.id_item) AS cantidad_items,

    CASE
        WHEN COUNT(i.id_item) = 0 THEN 1
        ELSE 0
    END AS flag_sin_items,

    CASE
        WHEN ABS(t.monto - COALESCE(SUM(i.cantidad * i.precio_unitario), 0)) > 1 THEN 1
        ELSE 0
    END AS flag_inconsistencia_monto,

    t.fecha_transaccion,
    t.fecha_proceso,

    CURRENT_TIMESTAMP AS fecha_carga_refinado
FROM curado.transacciones_curado t
LEFT JOIN curado.items_transaccion_curado i
    ON t.id_transaccion = i.id_transaccion
GROUP BY
    t.id_transaccion,
    t.id_cuenta,
    t.id_canal,
    t.id_estado,
    t.id_sucursal,
    t.monto,
    t.fecha_transaccion,
    t.fecha_proceso;