TRUNCATE TABLE curado.clientes_curado;
TRUNCATE TABLE curado.cuentas_curado;
TRUNCATE TABLE curado.productos_curado;
TRUNCATE TABLE curado.canales_curado;
TRUNCATE TABLE curado.sucursales_curado;
TRUNCATE TABLE curado.estados_transaccion_curado;
TRUNCATE TABLE curado.transacciones_curado;
TRUNCATE TABLE curado.items_transaccion_curado;

INSERT INTO curado.clientes_curado (
    id_cliente,
    nombre,
    dni,
    email,
    fecha_alta,
    fecha_carga_curado
)
SELECT
    r.id_cliente,
    r.nombre,
    r.dni,
    r.email,
    r.fecha_alta,
    CURRENT_TIMESTAMP AS fecha_carga_curado
FROM raw.clientes_raw r
WHERE r.id_cliente IS NOT NULL;

INSERT INTO curado.cuentas_curado (
    id_cuenta,
    id_cliente,
    tipo_cuenta,
    estado_cuenta,
    fecha_alta,
    fecha_carga_curado
)
SELECT
    r.id_cuenta,
    r.id_cliente,
    r.tipo_cuenta,
    r.estado_cuenta,
    r.fecha_alta,
    CURRENT_TIMESTAMP AS fecha_carga_curado
FROM raw.cuentas_raw r
INNER JOIN curado.clientes_curado c
    ON r.id_cliente = c.id_cliente
WHERE r.id_cuenta IS NOT NULL;

INSERT INTO curado.productos_curado (
    id_producto,
    nombre_producto,
    categoria,
    activo,
    fecha_carga_curado
)
SELECT
    r.id_producto,
    r.nombre_producto,
    r.categoria,
    r.activo,
    CURRENT_TIMESTAMP AS fecha_carga_curado
FROM raw.productos_raw r
WHERE r.id_producto IS NOT NULL;

INSERT INTO curado.canales_curado (
    id_canal,
    descripcion_canal,
    fecha_carga_curado
)
SELECT
    r.id_canal,
    r.descripcion_canal,
    CURRENT_TIMESTAMP AS fecha_carga_curado
FROM raw.canales_raw r
WHERE r.id_canal IS NOT NULL;

INSERT INTO curado.sucursales_curado (
    id_sucursal,
    nombre_sucursal,
    provincia,
    fecha_carga_curado
)
SELECT
    r.id_sucursal,
    r.nombre_sucursal,
    r.provincia,
    CURRENT_TIMESTAMP AS fecha_carga_curado
FROM raw.sucursales_raw r
WHERE r.id_sucursal IS NOT NULL;

INSERT INTO curado.estados_transaccion_curado (
    id_estado,
    descripcion_estado,
    es_final,
    fecha_carga_curado
)
SELECT
    r.id_estado,
    r.descripcion_estado,
    r.es_final,
    CURRENT_TIMESTAMP AS fecha_carga_curado
FROM raw.estados_transaccion_raw r
WHERE r.id_estado IS NOT NULL;

INSERT INTO curado.transacciones_curado (
    id_transaccion,
    id_cuenta,
    id_canal,
    id_estado,
    id_sucursal,
    monto,
    fecha_transaccion,
    fecha_proceso,
    fecha_carga_curado
)
SELECT
    r.id_transaccion,
    r.id_cuenta,
    r.id_canal,
    r.id_estado,
    r.id_sucursal,
    r.monto,
    r.fecha_transaccion,
    r.fecha_proceso,
    CURRENT_TIMESTAMP AS fecha_carga_curado
FROM raw.transacciones_raw r
INNER JOIN curado.cuentas_curado c
    ON r.id_cuenta = c.id_cuenta
INNER JOIN curado.canales_curado ca
    ON r.id_canal = ca.id_canal
INNER JOIN curado.estados_transaccion_curado e
    ON r.id_estado = e.id_estado
WHERE r.monto IS NOT NULL
  AND r.monto >= 0
  AND r.fecha_transaccion IS NOT NULL
  AND r.fecha_proceso IS NOT NULL;

INSERT INTO curado.items_transaccion_curado (
    id_item,
    id_transaccion,
    id_producto,
    cantidad,
    precio_unitario,
    fecha_carga_curado
)
SELECT
    r.id_item,
    r.id_transaccion,
    r.id_producto,
    r.cantidad,
    r.precio_unitario,
    CURRENT_TIMESTAMP AS fecha_carga_curado
FROM raw.items_transaccion_raw r
INNER JOIN curado.transacciones_curado t
    ON r.id_transaccion = t.id_transaccion
INNER JOIN curado.productos_curado p
    ON r.id_producto = p.id_producto
WHERE r.cantidad IS NOT NULL
  AND r.cantidad > 0
  AND r.precio_unitario IS NOT NULL
  AND r.precio_unitario > 0;
