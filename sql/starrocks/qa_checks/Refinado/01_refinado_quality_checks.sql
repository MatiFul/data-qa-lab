USE qa_lab_v3;

-- Resumen QA refinado
SELECT
    COUNT(*) AS total_transacciones,
    SUM(flag_sin_items) AS transacciones_sin_items,
    SUM(flag_inconsistencia_monto) AS transacciones_con_monto_inconsistente
FROM transacciones_refinado;

-- Top diferencias de monto
SELECT
    id_transaccion,
    monto_transaccion,
    monto_calculado_items,
    diferencia_monto,
    cantidad_items,
    flag_sin_items,
    flag_inconsistencia_monto
FROM transacciones_refinado
ORDER BY ABS(diferencia_monto) DESC
LIMIT 50;

-- Inconsistencias por canal
SELECT
    id_canal,
    COUNT(*) AS total,
    SUM(flag_inconsistencia_monto) AS inconsistencias
FROM transacciones_refinado
GROUP BY id_canal
ORDER BY inconsistencias DESC;