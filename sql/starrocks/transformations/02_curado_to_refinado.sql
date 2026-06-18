USE qa_lab_v3;

TRUNCATE TABLE transacciones_refinado;

INSERT INTO transacciones_refinado
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

    NOW() AS fecha_carga_refinado
FROM transacciones_curado t
LEFT JOIN items_transaccion_curado i
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