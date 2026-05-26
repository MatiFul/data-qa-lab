USE qa_lab_v3;

SELECT 'transacciones_raw' tabla, COUNT(*) registros FROM transacciones_raw
UNION ALL
SELECT 'transacciones_curado', COUNT(*) FROM transacciones_curado
UNION ALL
SELECT 'items_transaccion_raw', COUNT(*) FROM items_transaccion_raw
UNION ALL
SELECT 'items_transaccion_curado', COUNT(*) FROM items_transaccion_curado;

SELECT
    COUNT(*) AS total_transacciones_curado,
    SUM(CASE WHEN monto IS NULL THEN 1 ELSE 0 END) AS monto_null,
    SUM(CASE WHEN fecha_transaccion IS NULL THEN 1 ELSE 0 END) AS fecha_transaccion_null,
    SUM(CASE WHEN fecha_proceso IS NULL THEN 1 ELSE 0 END) AS fecha_proceso_null
FROM transacciones_curado;

SELECT
    COUNT(*) AS total_items_curado,
    SUM(CASE WHEN cantidad <= 0 OR cantidad IS NULL THEN 1 ELSE 0 END) AS cantidad_invalida,
    SUM(CASE WHEN precio_unitario <= 0 OR precio_unitario IS NULL THEN 1 ELSE 0 END) AS precio_invalido
FROM items_transaccion_curado;