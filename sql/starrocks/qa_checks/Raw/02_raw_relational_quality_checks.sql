USE qa_lab_v3;

-- Valida que toda transacción tenga una cuenta existente en cuentas_raw.
-- Detecta problemas de integridad referencial entre transacciones y cuentas.
SELECT COUNT(*) AS transacciones_con_cuenta_inexistente
FROM transacciones_raw t
LEFT JOIN cuentas_raw c
    ON t.id_cuenta = c.id_cuenta
WHERE c.id_cuenta IS NULL;

-- Valida que toda transacción tenga un canal existente en canales_raw.
-- Sirve para detectar códigos de canal inválidos o no catalogados.
SELECT COUNT(*) AS transacciones_con_canal_inexistente
FROM transacciones_raw t
LEFT JOIN canales_raw c
    ON t.id_canal = c.id_canal
WHERE c.id_canal IS NULL;

-- Valida que toda transacción tenga un estado existente en estados_transaccion_raw.
-- Detecta estados inválidos o fuera del catálogo esperado.
SELECT COUNT(*) AS transacciones_con_estado_inexistente
FROM transacciones_raw t
LEFT JOIN estados_transaccion_raw e
    ON t.id_estado = e.id_estado
WHERE e.id_estado IS NULL;

-- Valida transacciones sin detalle asociado en items_transaccion_raw.
-- En modelos 1:N, una transacción debería tener al menos un item.
SELECT COUNT(*) AS transacciones_sin_items
FROM transacciones_raw t
LEFT JOIN items_transaccion_raw i
    ON t.id_transaccion = i.id_transaccion
WHERE i.id_transaccion IS NULL;

-- Valida items que apuntan a una transacción inexistente.
-- Detecta problemas de integridad referencial desde el detalle hacia la cabecera.
SELECT COUNT(*) AS items_huerfanos
FROM items_transaccion_raw i
LEFT JOIN transacciones_raw t
    ON i.id_transaccion = t.id_transaccion
WHERE t.id_transaccion IS NULL;

-- Evidencia: ejemplos de transacciones sin items
SELECT
    t.id_transaccion,
    t.id_cuenta,
    t.id_canal,
    t.id_estado,
    t.monto,
    t.fecha_transaccion
FROM transacciones_raw t
LEFT JOIN items_transaccion_raw i ON t.id_transaccion = i.id_transaccion
WHERE i.id_transaccion IS NULL
LIMIT 50;