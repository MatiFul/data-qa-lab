import pytest


@pytest.mark.quality
@pytest.mark.parametrize(
    ("rule_name", "query"),
    [
        (
            "id_transaccion nulo o duplicado",
            """
            SELECT COUNT(*) - COUNT(DISTINCT id_transaccion)
                 + COUNT(*) FILTER (WHERE id_transaccion IS NULL)
            FROM raw.transacciones_raw
            """,
        ),
        (
            "id_item nulo o duplicado",
            """
            SELECT COUNT(*) - COUNT(DISTINCT id_item)
                 + COUNT(*) FILTER (WHERE id_item IS NULL)
            FROM raw.items_transaccion_raw
            """,
        ),
    ],
)
def test_raw_identifiers_are_complete_and_unique(db_scalar, rule_name, query):
    invalid_rows = db_scalar(query)
    assert invalid_rows == 0, f"{rule_name}: se detectaron {invalid_rows} filas"


@pytest.mark.quality
def test_raw_item_values_are_valid(db_scalar):
    invalid_items = db_scalar(
        """
        SELECT COUNT(*)
        FROM raw.items_transaccion_raw
        WHERE cantidad IS NULL
           OR cantidad <= 0
           OR precio_unitario IS NULL
           OR precio_unitario <= 0
        """
    )
    assert invalid_items == 0, f"Se detectaron {invalid_items} ítems inválidos"


@pytest.mark.quality
@pytest.mark.parametrize(
    ("relation_name", "query"),
    [
        (
            "cuenta",
            """
            SELECT COUNT(*)
            FROM raw.transacciones_raw transaction
            LEFT JOIN raw.cuentas_raw account
              ON account.id_cuenta = transaction.id_cuenta
            WHERE account.id_cuenta IS NULL
            """,
        ),
        (
            "canal",
            """
            SELECT COUNT(*)
            FROM raw.transacciones_raw transaction
            LEFT JOIN raw.canales_raw channel
              ON channel.id_canal = transaction.id_canal
            WHERE channel.id_canal IS NULL
            """,
        ),
        (
            "estado",
            """
            SELECT COUNT(*)
            FROM raw.transacciones_raw transaction
            LEFT JOIN raw.estados_transaccion_raw status
              ON status.id_estado = transaction.id_estado
            WHERE status.id_estado IS NULL
            """,
        ),
    ],
)
def test_raw_transaction_references_exist(db_scalar, relation_name, query):
    orphan_rows = db_scalar(query)
    assert orphan_rows == 0, (
        f"Se detectaron {orphan_rows} transacciones sin {relation_name} válido"
    )


@pytest.mark.quality
def test_raw_items_reference_an_existing_transaction(db_scalar):
    orphan_items = db_scalar(
        """
        SELECT COUNT(*)
        FROM raw.items_transaccion_raw item
        LEFT JOIN raw.transacciones_raw transaction
          ON transaction.id_transaccion = item.id_transaccion
        WHERE transaction.id_transaccion IS NULL
        """
    )
    assert orphan_items == 0, f"Se detectaron {orphan_items} ítems huérfanos"


@pytest.mark.quality
@pytest.mark.known_defect
@pytest.mark.xfail(
    strict=True,
    reason="Defecto controlado: RAW contiene montos nulos para practicar detección.",
)
def test_raw_transaction_amount_is_not_null(db_scalar):
    invalid_rows = db_scalar(
        "SELECT COUNT(*) FROM raw.transacciones_raw WHERE monto IS NULL"
    )
    assert invalid_rows == 0, f"Se detectaron {invalid_rows} montos nulos"


@pytest.mark.quality
@pytest.mark.known_defect
@pytest.mark.xfail(
    strict=True,
    reason="Defecto controlado: RAW contiene montos negativos.",
)
def test_raw_transaction_amount_is_non_negative(db_scalar):
    invalid_rows = db_scalar(
        "SELECT COUNT(*) FROM raw.transacciones_raw WHERE monto < 0"
    )
    assert invalid_rows == 0, f"Se detectaron {invalid_rows} montos negativos"


@pytest.mark.quality
@pytest.mark.known_defect
@pytest.mark.xfail(
    strict=True,
    reason="Defecto controlado: existen transacciones RAW sin detalle.",
)
def test_every_raw_transaction_has_items(db_scalar):
    transactions_without_items = db_scalar(
        """
        SELECT COUNT(*)
        FROM raw.transacciones_raw transaction
        LEFT JOIN raw.items_transaccion_raw item
          ON item.id_transaccion = transaction.id_transaccion
        WHERE item.id_transaccion IS NULL
        """
    )
    assert transactions_without_items == 0, (
        f"Se detectaron {transactions_without_items} transacciones sin ítems"
    )
