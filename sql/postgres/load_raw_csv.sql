TRUNCATE TABLE raw.clientes_raw;
TRUNCATE TABLE raw.cuentas_raw;
TRUNCATE TABLE raw.productos_raw;
TRUNCATE TABLE raw.estados_transaccion_raw;
TRUNCATE TABLE raw.canales_raw;
TRUNCATE TABLE raw.sucursales_raw;
TRUNCATE TABLE raw.transacciones_raw;
TRUNCATE TABLE raw.items_transaccion_raw;

COPY raw.clientes_raw
FROM '/tmp/output/clientes_raw.csv'
WITH (FORMAT csv, HEADER true);

COPY raw.cuentas_raw
FROM '/tmp/output/cuentas_raw.csv'
WITH (FORMAT csv, HEADER true);

COPY raw.productos_raw
FROM '/tmp/output/productos_raw.csv'
WITH (FORMAT csv, HEADER true);

COPY raw.estados_transaccion_raw
FROM '/tmp/output/estados_transaccion_raw.csv'
WITH (FORMAT csv, HEADER true);

COPY raw.canales_raw
FROM '/tmp/output/canales_raw.csv'
WITH (FORMAT csv, HEADER true);

COPY raw.sucursales_raw
FROM '/tmp/output/sucursales_raw.csv'
WITH (FORMAT csv, HEADER true);

COPY raw.transacciones_raw
FROM '/tmp/output/transacciones_raw.csv'
WITH (FORMAT csv, HEADER true);

COPY raw.items_transaccion_raw
FROM '/tmp/output/items_transaccion_raw.csv'
WITH (FORMAT csv, HEADER true);