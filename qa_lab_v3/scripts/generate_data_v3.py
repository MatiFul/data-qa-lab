import csv
import random
from datetime import datetime, timedelta

# CONFIG
NUM_CLIENTES = 10
NUM_PRODUCTOS = 10
NUM_TRANSACCIONES = 100

# ---- CLIENTES ----
clientes = []
for i in range(1, NUM_CLIENTES + 1):
    clientes.append([i, f"Cliente_{i}", "DNI", 30000000 + i, "2025-01-01", random.randint(1,3)])

# error: cliente sin id
clientes.append([None, "Cliente_error", "DNI", 99999999, "2025-01-01", 1])

# ---- CUENTAS ----
cuentas = []
for i in range(1, NUM_CLIENTES + 1):
    cuentas.append([i, i, "CA", "ARS", "2025-01-01", "ACTIVA"])

# error: cliente inexistente
cuentas.append([999, 9999, "CA", "ARS", "2025-01-01", "ACTIVA"])

# ---- PRODUCTOS ----
productos = []
for i in range(1, NUM_PRODUCTOS + 1):
    precio = round(random.uniform(100, 5000), 2)
    productos.append([i, f"Producto_{i}", "categoria", precio, "S"])

# error: precio negativo
productos.append([999, "Producto_error", "categoria", -100, "S"])

# ---- CANALES ----
canales = [
    [1, "ATM", "FISICO", "S"],
    [2, "HBI", "DIGITAL", "S"],
    [3, "MODO", "DIGITAL", "S"]
]

# ---- SUCURSALES ----
sucursales = [
    [1, "Sucursal_1", "Buenos Aires", "AMBA", "S"],
    [2, "Sucursal_2", "Cordoba", "Interior", "S"],
    [3, "Sucursal_3", "Santa Fe", "Interior", "S"]
]

# ---- ESTADOS ----
estados = [
    [1, "APROBADA", "S"],
    [2, "RECHAZADA", "S"],
    [3, "PENDIENTE", "N"]
]

# ---- TRANSACCIONES ----
transacciones = []
base_date = datetime(2025, 1, 1)

for i in range(1, NUM_TRANSACCIONES + 1):
    fecha = base_date + timedelta(days=random.randint(0, 29))
    monto = round(random.uniform(100, 10000), 2)

    transacciones.append([
        i,
        random.randint(1, NUM_CLIENTES),
        random.randint(1, 3),
        random.randint(1, 3),
        monto,
        fecha.strftime("%Y-%m-%d"),
        fecha.strftime("%Y-%m-%d")
    ])

# errores
transacciones.append([2000, 999, 1, 1, 1000, "2025-01-01", "2025-01-01"])  # cuenta inexistente
transacciones.append([2001, 1, 1, 1, -500, "2025-01-01", "2025-01-01"])   # monto negativo

# ---- ITEMS ----
items = []
for i in range(1, 200):
    items.append([
        i,
        random.randint(1, NUM_TRANSACCIONES),
        random.randint(1, NUM_PRODUCTOS),
        random.randint(1, 5),
        round(random.uniform(100, 1000), 2)
    ])

# error FK
items.append([9999, 9999, 1, 1, 100])

# ---- WRITE ----
def write_csv(name, headers, data):
    with open(f"../data/{name}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)

write_csv("clientes_raw", ["id_cliente","nombre","tipo_documento","nro_documento","fecha_alta","id_sucursal"], clientes)
write_csv("cuentas_raw", ["id_cuenta","id_cliente","tipo_cuenta","moneda","fecha_alta","estado_cuenta"], cuentas)
write_csv("productos_raw", ["id_producto","nombre_producto","categoria","precio_base","activo"], productos)
write_csv("canales_raw", ["id_canal","nombre_canal","tipo_canal","activo"], canales)
write_csv("sucursales_raw", ["id_sucursal","nombre_sucursal","provincia","region","activo"], sucursales)
write_csv("estados_transaccion_raw", ["id_estado","descripcion_estado","es_final"], estados)
write_csv("transacciones_raw", ["id_transaccion","id_cuenta","id_canal","id_estado","monto","fecha_transaccion","fecha_proceso"], transacciones)
write_csv("items_transaccion_raw", ["id_item","id_transaccion","id_producto","cantidad","precio_unitario"], items)