from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

fake = Faker("es_AR")
random.seed(42)

OUTPUT_DIR = "output"

N_CLIENTES = 500
N_CUENTAS = 700
N_PRODUCTOS = 50
N_TRANSACCIONES = 5000
N_ITEMS = 12000

def random_date():
    start = datetime(2025, 1, 1)
    end = datetime(2025, 3, 31)
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days), seconds=random.randint(0, 86399))

clientes = []
for i in range(1, N_CLIENTES + 1):
    clientes.append({
        "id_cliente": i,
        "nombre": fake.name(),
        "dni": random.randint(20000000, 45000000),
        "email": fake.email(),
        "fecha_alta": fake.date_between(start_date="-5y", end_date="-30d")
    })

cuentas = []
for i in range(1, N_CUENTAS + 1):
    cuentas.append({
        "id_cuenta": i,
        "id_cliente": random.randint(1, N_CLIENTES),
        "tipo_cuenta": random.choice(["CAJA_AHORRO", "CUENTA_CORRIENTE"]),
        "estado_cuenta": random.choice(["ACTIVA", "ACTIVA", "ACTIVA", "BLOQUEADA", "CERRADA"]),
        "fecha_alta": fake.date_between(start_date="-5y", end_date="-30d")
    })

productos = []
for i in range(1, N_PRODUCTOS + 1):
    productos.append({
        "id_producto": i,
        "nombre_producto": random.choice(["Transferencia", "Pago Servicio", "Extraccion ATM", "Compra Debito", "Impuesto", "Seguro"]) + f" {i}",
        "categoria": random.choice(["PAGOS", "ATM", "TRANSFERENCIAS", "COMPRAS", "SERVICIOS"]),
        "activo": random.choice([1, 1, 1, 0])
    })

estados = [
    {"id_estado": 1, "descripcion_estado": "APROBADA", "es_final": 1},
    {"id_estado": 2, "descripcion_estado": "RECHAZADA", "es_final": 1},
    {"id_estado": 3, "descripcion_estado": "PENDIENTE", "es_final": 0},
    {"id_estado": 4, "descripcion_estado": "REVERSADA", "es_final": 1},
]

canales = [
    {"id_canal": 1, "descripcion_canal": "HBI"},
    {"id_canal": 2, "descripcion_canal": "HBE"},
    {"id_canal": 3, "descripcion_canal": "ATM"},
    {"id_canal": 4, "descripcion_canal": "MODO"},
    {"id_canal": 5, "descripcion_canal": "SUCURSAL"},
]

sucursales = []
for i in range(1, 21):
    sucursales.append({
        "id_sucursal": i,
        "nombre_sucursal": f"Sucursal {i}",
        "provincia": random.choice(["CABA", "Buenos Aires", "Santa Fe", "Entre Rios", "San Juan", "Cordoba"])
    })

transacciones = []
for i in range(1, N_TRANSACCIONES + 1):
    monto = round(random.uniform(500, 150000), 2)

    # errores intencionales
    if random.random() < 0.02:
        monto = None
    elif random.random() < 0.015:
        monto = -monto

    transacciones.append({
        "id_transaccion": i,
        "id_cuenta": random.randint(1, N_CUENTAS),
        "id_canal": random.randint(1, 5),
        "id_estado": random.choice([1, 1, 1, 1, 2, 3, 4]),
        "id_sucursal": random.randint(1, 20),
        "monto": monto,
        "fecha_transaccion": random_date(),
        "fecha_proceso": random_date().date()
    })

items = []
for i in range(1, N_ITEMS + 1):
    items.append({
        "id_item": i,
        "id_transaccion": random.randint(1, N_TRANSACCIONES),
        "id_producto": random.randint(1, N_PRODUCTOS),
        "cantidad": random.randint(1, 5),
        "precio_unitario": round(random.uniform(100, 50000), 2)
    })

pd.DataFrame(clientes).to_csv(f"{OUTPUT_DIR}/clientes_raw.csv", index=False)
pd.DataFrame(cuentas).to_csv(f"{OUTPUT_DIR}/cuentas_raw.csv", index=False)
pd.DataFrame(productos).to_csv(f"{OUTPUT_DIR}/productos_raw.csv", index=False)
pd.DataFrame(estados).to_csv(f"{OUTPUT_DIR}/estados_transaccion_raw.csv", index=False)
pd.DataFrame(canales).to_csv(f"{OUTPUT_DIR}/canales_raw.csv", index=False)
pd.DataFrame(sucursales).to_csv(f"{OUTPUT_DIR}/sucursales_raw.csv", index=False)
pd.DataFrame(transacciones).to_csv(f"{OUTPUT_DIR}/transacciones_raw.csv", index=False)
pd.DataFrame(items).to_csv(f"{OUTPUT_DIR}/items_transaccion_raw.csv", index=False)

print("Dataset generado correctamente.")