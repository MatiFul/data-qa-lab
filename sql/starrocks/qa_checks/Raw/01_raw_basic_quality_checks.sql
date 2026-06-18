USE qa_lab_v3;

-- Validación básica de volumen por tabla RAW.
-- Permite verificar que la carga masiva fue exitosa
-- y detectar diferencias inesperadas entre tablas.
SELECT 'clientes_raw' tabla, COUNT(*) registros FROM clientes_raw
UNION ALL
SELECT 'cuentas_raw', COUNT(*) FROM cuentas_raw
UNION ALL
SELECT 'productos_raw', COUNT(*) FROM productos_raw
UNION ALL
SELECT 'transacciones_raw', COUNT(*) FROM transacciones_raw
UNION ALL
SELECT 'items_transaccion_raw', COUNT(*) FROM items_transaccion_raw
UNION ALL
SELECT 'sucursales_raw', COUNT(*) FROM sucursales_raw
UNION ALL
SELECT 'canales_raw', COUNT(*) FROM canales_raw
UNION ALL
SELECT 'estados_transaccion_raw', COUNT(*) FROM estados_transaccion_raw;

-- Validación de calidad sobre transacciones RAW.
-- Se controlan:
-- - montos nulos
-- - montos negativos
-- - fechas faltantes
-- Este tipo de check suele ejecutarse antes del curado.
SELECT
    COUNT(*) AS total_transacciones,
    SUM(CASE WHEN monto IS NULL THEN 1 ELSE 0 END) AS monto_null,
    SUM(CASE WHEN monto < 0 THEN 1 ELSE 0 END) AS monto_negativo,
    SUM(CASE WHEN fecha_transaccion IS NULL THEN 1 ELSE 0 END) AS fecha_transaccion_null,
    SUM(CASE WHEN fecha_proceso IS NULL THEN 1 ELSE 0 END) AS fecha_proceso_null
FROM transacciones_raw;

-- Validación de calidad sobre items de transacción.
-- Se controlan:
-- - cantidades inválidas
-- - precios nulos
-- - precios menores o iguales a cero
-- Actualmente el dataset no contiene anomalías intencionales en items.
SELECT
    COUNT(*) AS total_items,
    SUM(CASE WHEN cantidad IS NULL THEN 1 ELSE 0 END) AS cantidad_null,
    SUM(CASE WHEN cantidad <= 0 THEN 1 ELSE 0 END) AS cantidad_invalida,
    SUM(CASE WHEN precio_unitario IS NULL THEN 1 ELSE 0 END) AS precio_null,
    SUM(CASE WHEN precio_unitario <= 0 THEN 1 ELSE 0 END) AS precio_invalido
FROM items_transaccion_raw;

