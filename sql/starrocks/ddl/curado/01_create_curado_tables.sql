USE qa_lab_v3;

DROP TABLE IF EXISTS transacciones_curado;

CREATE TABLE transacciones_curado (
    id_transaccion INT NULL,
    id_cuenta INT NULL,
    id_canal INT NULL,
    id_estado INT NULL,
    id_sucursal INT NULL,
    monto DECIMAL(12,2) NULL,
    fecha_transaccion DATETIME NULL,
    fecha_proceso DATE NULL,
    fecha_carga_curado DATETIME NULL
)
ENGINE=OLAP
DUPLICATE KEY(id_transaccion)
DISTRIBUTED BY HASH(id_transaccion) BUCKETS 5
PROPERTIES (
    "replication_num" = "1"
);

DROP TABLE IF EXISTS items_transaccion_curado;

CREATE TABLE items_transaccion_curado (
    id_item INT NULL,
    id_transaccion INT NULL,
    id_producto INT NULL,
    cantidad INT NULL,
    precio_unitario DECIMAL(12,2) NULL,
    fecha_carga_curado DATETIME NULL
)
ENGINE=OLAP
DUPLICATE KEY(id_item)
DISTRIBUTED BY HASH(id_item) BUCKETS 5
PROPERTIES (
    "replication_num" = "1"
);

DROP TABLE IF EXISTS clientes_curado;
CREATE TABLE clientes_curado (
    id_cliente INT NULL,
    nombre STRING NULL,
    dni BIGINT NULL,
    email STRING NULL,
    fecha_alta DATE NULL,
    fecha_carga_curado DATETIME NULL
)
ENGINE=OLAP
DUPLICATE KEY(id_cliente)
DISTRIBUTED BY HASH(id_cliente) BUCKETS 5
PROPERTIES ("replication_num" = "1");

DROP TABLE IF EXISTS cuentas_curado;
CREATE TABLE cuentas_curado (
    id_cuenta INT NULL,
    id_cliente INT NULL,
    tipo_cuenta STRING NULL,
    estado_cuenta STRING NULL,
    fecha_alta DATE NULL,
    fecha_carga_curado DATETIME NULL
)
ENGINE=OLAP
DUPLICATE KEY(id_cuenta)
DISTRIBUTED BY HASH(id_cuenta) BUCKETS 5
PROPERTIES ("replication_num" = "1");

DROP TABLE IF EXISTS productos_curado;
CREATE TABLE productos_curado (
    id_producto INT NULL,
    nombre_producto STRING NULL,
    categoria STRING NULL,
    activo INT NULL,
    fecha_carga_curado DATETIME NULL
)
ENGINE=OLAP
DUPLICATE KEY(id_producto)
DISTRIBUTED BY HASH(id_producto) BUCKETS 5
PROPERTIES ("replication_num" = "1");

DROP TABLE IF EXISTS canales_curado;
CREATE TABLE canales_curado (
    id_canal INT NULL,
    descripcion_canal STRING NULL,
    fecha_carga_curado DATETIME NULL
)
ENGINE=OLAP
DUPLICATE KEY(id_canal)
DISTRIBUTED BY HASH(id_canal) BUCKETS 1
PROPERTIES ("replication_num" = "1");

DROP TABLE IF EXISTS sucursales_curado;
CREATE TABLE sucursales_curado (
    id_sucursal INT NULL,
    nombre_sucursal STRING NULL,
    provincia STRING NULL,
    fecha_carga_curado DATETIME NULL
)
ENGINE=OLAP
DUPLICATE KEY(id_sucursal)
DISTRIBUTED BY HASH(id_sucursal) BUCKETS 1
PROPERTIES ("replication_num" = "1");

DROP TABLE IF EXISTS estados_transaccion_curado;
CREATE TABLE estados_transaccion_curado (
    id_estado INT NULL,
    descripcion_estado STRING NULL,
    es_final INT NULL,
    fecha_carga_curado DATETIME NULL
)
ENGINE=OLAP
DUPLICATE KEY(id_estado)
DISTRIBUTED BY HASH(id_estado) BUCKETS 1
PROPERTIES ("replication_num" = "1");