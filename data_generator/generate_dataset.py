from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import random

from faker import Faker
import pandas as pd


SEED = 42
N_CLIENTES = 500
N_CUENTAS = 700
N_PRODUCTOS = 50
N_TRANSACCIONES = 5000
N_ITEMS = 12000

# Anomalías controladas. Los grupos no se superponen.
N_MONTOS_NULOS = 100
N_MONTOS_NEGATIVOS = 75
N_TRANSACCIONES_SIN_ITEMS = 100
N_MONTOS_INCONSISTENTES = 100

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
MONEY_QUANTIZER = Decimal("0.01")

random.seed(SEED)
Faker.seed(SEED)
fake = Faker("es_AR")
fake.seed_instance(SEED)


def random_date() -> datetime:
    start = datetime(2025, 1, 1)
    end = datetime(2025, 3, 31)
    delta = end - start
    return start + timedelta(
        days=random.randint(0, delta.days),
        seconds=random.randint(0, 86399),
    )


def random_money(minimum: int, maximum: int) -> Decimal:
    return Decimal(str(random.uniform(minimum, maximum))).quantize(
        MONEY_QUANTIZER,
        rounding=ROUND_HALF_UP,
    )


def take_ids(available_ids: set[int], amount: int) -> set[int]:
    selected = set(random.sample(sorted(available_ids), amount))
    available_ids.difference_update(selected)
    return selected


clientes = []
for customer_id in range(1, N_CLIENTES + 1):
    clientes.append(
        {
            "id_cliente": customer_id,
            "nombre": fake.name(),
            "dni": random.randint(20000000, 45000000),
            "email": fake.email(),
            "fecha_alta": fake.date_between(start_date="-5y", end_date="-30d"),
        }
    )

cuentas = []
for account_id in range(1, N_CUENTAS + 1):
    cuentas.append(
        {
            "id_cuenta": account_id,
            "id_cliente": random.randint(1, N_CLIENTES),
            "tipo_cuenta": random.choice(["CAJA_AHORRO", "CUENTA_CORRIENTE"]),
            "estado_cuenta": random.choice(
                ["ACTIVA", "ACTIVA", "ACTIVA", "BLOQUEADA", "CERRADA"]
            ),
            "fecha_alta": fake.date_between(start_date="-5y", end_date="-30d"),
        }
    )

productos = []
for product_id in range(1, N_PRODUCTOS + 1):
    productos.append(
        {
            "id_producto": product_id,
            "nombre_producto": random.choice(
                [
                    "Transferencia",
                    "Pago Servicio",
                    "Extraccion ATM",
                    "Compra Debito",
                    "Impuesto",
                    "Seguro",
                ]
            )
            + f" {product_id}",
            "categoria": random.choice(
                ["PAGOS", "ATM", "TRANSFERENCIAS", "COMPRAS", "SERVICIOS"]
            ),
            "activo": random.choice([1, 1, 1, 0]),
        }
    )

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
for branch_id in range(1, 21):
    sucursales.append(
        {
            "id_sucursal": branch_id,
            "nombre_sucursal": f"Sucursal {branch_id}",
            "provincia": random.choice(
                [
                    "CABA",
                    "Buenos Aires",
                    "Santa Fe",
                    "Entre Rios",
                    "San Juan",
                    "Cordoba",
                ]
            ),
        }
    )

all_transaction_ids = set(range(1, N_TRANSACCIONES + 1))
available_anomaly_ids = set(all_transaction_ids)

null_amount_ids = take_ids(available_anomaly_ids, N_MONTOS_NULOS)
negative_amount_ids = take_ids(available_anomaly_ids, N_MONTOS_NEGATIVOS)
missing_item_ids = take_ids(available_anomaly_ids, N_TRANSACCIONES_SIN_ITEMS)
inconsistent_amount_ids = take_ids(
    available_anomaly_ids,
    N_MONTOS_INCONSISTENTES,
)

eligible_item_transaction_ids = sorted(all_transaction_ids - missing_item_ids)
item_totals = {
    transaction_id: Decimal("0.00") for transaction_id in all_transaction_ids
}
items = []


def add_item(transaction_id: int) -> None:
    quantity = random.randint(1, 5)
    unit_price = random_money(100, 50000)
    item_id = len(items) + 1

    items.append(
        {
            "id_item": item_id,
            "id_transaccion": transaction_id,
            "id_producto": random.randint(1, N_PRODUCTOS),
            "cantidad": quantity,
            "precio_unitario": unit_price,
        }
    )
    item_totals[transaction_id] += quantity * unit_price


# Cada transacción válida recibe primero un ítem.
for transaction_id in eligible_item_transaction_ids:
    add_item(transaction_id)

# Los ítems restantes se distribuyen entre transacciones que ya tienen detalle.
for _ in range(N_ITEMS - len(items)):
    add_item(random.choice(eligible_item_transaction_ids))

transacciones = []
for transaction_id in range(1, N_TRANSACCIONES + 1):
    calculated_amount = item_totals[transaction_id].quantize(MONEY_QUANTIZER)

    if transaction_id in null_amount_ids:
        amount = None
    elif transaction_id in negative_amount_ids:
        amount = -calculated_amount
    elif transaction_id in missing_item_ids:
        amount = random_money(500, 150000)
    elif transaction_id in inconsistent_amount_ids:
        amount = calculated_amount + random_money(10, 5000)
    else:
        amount = calculated_amount

    transacciones.append(
        {
            "id_transaccion": transaction_id,
            "id_cuenta": random.randint(1, N_CUENTAS),
            "id_canal": random.randint(1, 5),
            "id_estado": random.choice([1, 1, 1, 1, 2, 3, 4]),
            "id_sucursal": random.randint(1, 20),
            "monto": amount,
            "fecha_transaccion": random_date(),
            "fecha_proceso": random_date().date(),
        }
    )

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

pd.DataFrame(clientes).to_csv(OUTPUT_DIR / "clientes_raw.csv", index=False)
pd.DataFrame(cuentas).to_csv(OUTPUT_DIR / "cuentas_raw.csv", index=False)
pd.DataFrame(productos).to_csv(OUTPUT_DIR / "productos_raw.csv", index=False)
pd.DataFrame(estados).to_csv(
    OUTPUT_DIR / "estados_transaccion_raw.csv",
    index=False,
)
pd.DataFrame(canales).to_csv(OUTPUT_DIR / "canales_raw.csv", index=False)
pd.DataFrame(sucursales).to_csv(OUTPUT_DIR / "sucursales_raw.csv", index=False)
pd.DataFrame(transacciones).to_csv(
    OUTPUT_DIR / "transacciones_raw.csv",
    index=False,
)
pd.DataFrame(items).to_csv(
    OUTPUT_DIR / "items_transaccion_raw.csv",
    index=False,
)

print("Dataset generado correctamente.")
print(f"Semilla: {SEED}")
print(f"Transacciones: {len(transacciones)}")
print(f"Ítems: {len(items)}")
print(f"Montos nulos controlados: {len(null_amount_ids)}")
print(f"Montos negativos controlados: {len(negative_amount_ids)}")
print(f"Transacciones sin ítems controladas: {len(missing_item_ids)}")
print(f"Montos inconsistentes controlados: {len(inconsistent_amount_ids)}")
