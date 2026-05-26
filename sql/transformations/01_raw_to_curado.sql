USE qa_lab_v3;

TRUNCATE TABLE clientes_curado;
TRUNCATE TABLE cuentas_curado;
TRUNCATE TABLE productos_curado;
TRUNCATE TABLE canales_curado;
TRUNCATE TABLE sucursales_curado;
TRUNCATE TABLE estados_transaccion_curado;
TRUNCATE TABLE transacciones_curado;
TRUNCATE TABLE items_transaccion_curado;

INSERT INTO clientes_curado
SELECT
    id_cliente,
    nombre,
    dni,
    email,
    fecha_alta,
    NOW()
FROM clientes_raw
WHERE id_cliente IS NOT NULL;

INSERT INTO cuentas_curado
SELECT
    c.id_cuenta,
    c.id_cliente,
    c.tipo_cuenta,
    c.estado_cuenta,
    c.fecha_alta,
    NOW()
FROM cuentas_raw c
INNER JOIN clientes_curado cl
    ON c.id_cliente = cl.id_cliente
WHERE c.id_cuenta IS NOT NULL;

INSERT INTO productos_curado
SELECT
    id_producto,
    nombre_producto,
    categoria,
    activo,
    NOW()
FROM productos_raw
WHERE id_producto IS NOT NULL;

INSERT INTO canales_curado
SELECT
    id_canal,
    descripcion_canal,
    NOW()
FROM canales_raw
WHERE id_canal IS NOT NULL;

INSERT INTO sucursales_curado
SELECT
    id_sucursal,
    nombre_sucursal,
    provincia,
    NOW()
FROM sucursales_raw
WHERE id_sucursal IS NOT NULL;

INSERT INTO estados_transaccion_curado
SELECT
    id_estado,
    descripcion_estado,
    es_final,
    NOW()
FROM estados_transaccion_raw
WHERE id_estado IS NOT NULL;

INSERT INTO transacciones_curado
SELECT
    t.id_transaccion,
    t.id_cuenta,
    t.id_canal,
    t.id_estado,
    t.id_sucursal,
    t.monto,
    t.fecha_transaccion,
    t.fecha_proceso,
    NOW() AS fecha_carga_curado
FROM transacciones_raw t
INNER JOIN cuentas_raw c ON t.id_cuenta = c.id_cuenta
INNER JOIN canales_raw ca ON t.id_canal = ca.id_canal
INNER JOIN estados_transaccion_raw e ON t.id_estado = e.id_estado
WHERE t.monto IS NOT NULL
  AND t.fecha_transaccion IS NOT NULL
  AND t.fecha_proceso IS NOT NULL;

INSERT INTO items_transaccion_curado
SELECT
    i.id_item,
    i.id_transaccion,
    i.id_producto,
    i.cantidad,
    i.precio_unitario,
    NOW() AS fecha_carga_curado
FROM items_transaccion_raw i
INNER JOIN transacciones_curado t ON i.id_transaccion = t.id_transaccion
INNER JOIN productos_raw p ON i.id_producto = p.id_producto
WHERE i.cantidad IS NOT NULL
  AND i.cantidad > 0
  AND i.precio_unitario IS NOT NULL
  AND i.precio_unitario > 0;