USE qa_lab_v3;

DROP TABLE IF EXISTS clientes_raw;
CREATE TABLE clientes_raw (
    id_cliente INT NULL,
    nombre STRING NULL,
    dni BIGINT NULL,
    email STRING NULL,
    fecha_alta DATE NULL
)
ENGINE=OLAP
DUPLICATE KEY(id_cliente)
DISTRIBUTED BY HASH(id_cliente) BUCKETS 5
PROPERTIES (
    "replication_num" = "1"
);

DROP TABLE IF EXISTS cuentas_raw;
CREATE TABLE cuentas_raw (
    id_cuenta INT NULL,
    id_cliente INT NULL,
    tipo_cuenta STRING NULL,
    estado_cuenta STRING NULL,
    fecha_alta DATE NULL
)
ENGINE=OLAP
DUPLICATE KEY(id_cuenta)
DISTRIBUTED BY HASH(id_cuenta) BUCKETS 5
PROPERTIES (
    "replication_num" = "1"
);

DROP TABLE IF EXISTS productos_raw;
CREATE TABLE productos_raw (
    id_producto INT NULL,
    nombre_producto STRING NULL,
    categoria STRING NULL,
    activo INT NULL
)
ENGINE=OLAP
DUPLICATE KEY(id_producto)
DISTRIBUTED BY HASH(id_producto) BUCKETS 5
PROPERTIES (
    "replication_num" = "1"
);

DROP TABLE IF EXISTS estados_transaccion_raw;
CREATE TABLE estados_transaccion_raw (
    id_estado INT NULL,
    descripcion_estado STRING NULL,
    es_final INT NULL
)
ENGINE=OLAP
DUPLICATE KEY(id_estado)
DISTRIBUTED BY HASH(id_estado) BUCKETS 1
PROPERTIES (
    "replication_num" = "1"
);

DROP TABLE IF EXISTS canales_raw;
CREATE TABLE canales_raw (
    id_canal INT NULL,
    descripcion_canal STRING NULL
)
ENGINE=OLAP
DUPLICATE KEY(id_canal)
DISTRIBUTED BY HASH(id_canal) BUCKETS 1
PROPERTIES (
    "replication_num" = "1"
);

DROP TABLE IF EXISTS sucursales_raw;
CREATE TABLE sucursales_raw (
    id_sucursal INT NULL,
    nombre_sucursal STRING NULL,
    provincia STRING NULL
)
ENGINE=OLAP
DUPLICATE KEY(id_sucursal)
DISTRIBUTED BY HASH(id_sucursal) BUCKETS 1
PROPERTIES (
    "replication_num" = "1"
);

DROP TABLE IF EXISTS transacciones_raw;
CREATE TABLE transacciones_raw (
    id_transaccion INT NULL,
    id_cuenta INT NULL,
    id_canal INT NULL,
    id_estado INT NULL,
    id_sucursal INT NULL,
    monto DECIMAL(12,2) NULL,
    fecha_transaccion DATETIME NULL,
    fecha_proceso DATE NULL
)
ENGINE=OLAP
DUPLICATE KEY(id_transaccion)
DISTRIBUTED BY HASH(id_transaccion) BUCKETS 5
PROPERTIES (
    "replication_num" = "1"
);

DROP TABLE IF EXISTS items_transaccion_raw;
CREATE TABLE items_transaccion_raw (
    id_item INT NULL,
    id_transaccion INT NULL,
    id_producto INT NULL,
    cantidad INT NULL,
    precio_unitario DECIMAL(12,2) NULL
)
ENGINE=OLAP
DUPLICATE KEY(id_item)
DISTRIBUTED BY HASH(id_item) BUCKETS 5
PROPERTIES (
    "replication_num" = "1"
);