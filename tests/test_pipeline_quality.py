import os

import pytest


@pytest.mark.quality
def test_pipeline_transaction_counts_are_reconciled(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM raw.transacciones_raw),
                (SELECT COUNT(*) FROM curado.transacciones_curado),
                (SELECT COUNT(*) FROM refinado.transacciones_refinado),
                (SELECT COUNT(*) FROM consumo.transacciones_consumo)
            """
        )
        raw_count, curated_count, refined_count, consumption_count = cursor.fetchone()

    assert raw_count >= curated_count > 0
    assert curated_count == refined_count == consumption_count


@pytest.mark.quality
def test_curated_required_transaction_values_are_complete(db_scalar):
    invalid_rows = db_scalar(
        """
        SELECT COUNT(*)
        FROM curado.transacciones_curado
        WHERE id_transaccion IS NULL
           OR id_cuenta IS NULL
           OR id_canal IS NULL
           OR id_estado IS NULL
           OR monto IS NULL
           OR fecha_transaccion IS NULL
           OR fecha_proceso IS NULL
        """
    )
    assert invalid_rows == 0, (
        f"Se detectaron {invalid_rows} transacciones curadas incompletas"
    )


@pytest.mark.quality
def test_curated_items_are_valid_and_referenced(db_scalar):
    invalid_rows = db_scalar(
        """
        SELECT COUNT(*)
        FROM curado.items_transaccion_curado item
        LEFT JOIN curado.transacciones_curado transaction
          ON transaction.id_transaccion = item.id_transaccion
        LEFT JOIN curado.productos_curado product
          ON product.id_producto = item.id_producto
        WHERE item.cantidad IS NULL
           OR item.cantidad <= 0
           OR item.precio_unitario IS NULL
           OR item.precio_unitario <= 0
           OR transaction.id_transaccion IS NULL
           OR product.id_producto IS NULL
        """
    )
    assert invalid_rows == 0, f"Se detectaron {invalid_rows} ítems curados inválidos"


@pytest.mark.quality
def test_refined_quality_flags_match_the_calculations(db_scalar):
    invalid_flags = db_scalar(
        """
        SELECT COUNT(*)
        FROM refinado.transacciones_refinado
        WHERE flag_sin_items IS DISTINCT FROM
              CASE WHEN cantidad_items = 0 THEN 1 ELSE 0 END
           OR flag_inconsistencia_monto IS DISTINCT FROM
              CASE WHEN ABS(diferencia_monto) > 1 THEN 1 ELSE 0 END
        """
    )
    assert invalid_flags == 0, (
        f"Se detectaron {invalid_flags} flags de calidad calculados incorrectamente"
    )


@pytest.mark.quality
def test_refined_and_consumption_layers_are_consistent(db_scalar):
    inconsistent_rows = db_scalar(
        """
        SELECT COUNT(*)
        FROM refinado.transacciones_refinado refined
        FULL OUTER JOIN consumo.transacciones_consumo consumption
          USING (id_transaccion)
        WHERE refined.id_transaccion IS NULL
           OR consumption.id_transaccion IS NULL
           OR refined.monto_transaccion IS DISTINCT FROM
              consumption.monto_transaccion
           OR refined.monto_calculado_items IS DISTINCT FROM
              consumption.monto_calculado_items
           OR refined.flag_sin_items IS DISTINCT FROM
              consumption.flag_sin_items
           OR refined.flag_inconsistencia_monto IS DISTINCT FROM
              consumption.flag_inconsistencia_monto
        """
    )
    assert inconsistent_rows == 0, (
        f"Se detectaron {inconsistent_rows} diferencias entre refinado y consumo"
    )


@pytest.mark.quality
def test_consumption_date_dimensions_are_correct(db_scalar):
    invalid_dates = db_scalar(
        """
        SELECT COUNT(*)
        FROM consumo.transacciones_consumo
        WHERE anio_transaccion IS DISTINCT FROM
              EXTRACT(YEAR FROM fecha_transaccion)::INT
           OR mes_transaccion IS DISTINCT FROM
              EXTRACT(MONTH FROM fecha_transaccion)::INT
           OR dia_transaccion IS DISTINCT FROM
              EXTRACT(DAY FROM fecha_transaccion)::INT
        """
    )
    assert invalid_dates == 0, (
        f"Se detectaron {invalid_dates} dimensiones de fecha incorrectas"
    )


@pytest.mark.quality
def test_curated_transaction_amount_is_non_negative(db_scalar):
    invalid_rows = db_scalar(
        "SELECT COUNT(*) FROM curado.transacciones_curado WHERE monto < 0"
    )
    assert invalid_rows == 0, (
        f"Se detectaron {invalid_rows} montos negativos en la capa curada"
    )


@pytest.mark.quality
def test_refined_inconsistency_rate_is_controlled(db_connection):
    max_inconsistency_rate = float(
        os.getenv("QA_MAX_INCONSISTENCY_RATE", "0.05")
    )
    assert 0 < max_inconsistency_rate <= 1, (
        "QA_MAX_INCONSISTENCY_RATE debe ser un decimal mayor que 0 "
        "y menor o igual que 1"
    )

    with db_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                COUNT(*) FILTER (WHERE flag_inconsistencia_monto = 1),
                COUNT(*)
            FROM refinado.transacciones_refinado
            """
        )
        inconsistent_rows, total_rows = cursor.fetchone()

    inconsistency_rate = inconsistent_rows / total_rows
    assert 0 < inconsistency_rate <= max_inconsistency_rate, (
        "La tasa de montos inconsistentes debe existir como anomalía controlada "
        f"y no superar el {max_inconsistency_rate:.2%}. "
        f"Tasa actual: {inconsistency_rate:.2%}"
    )


@pytest.mark.quality
@pytest.mark.known_defect
@pytest.mark.xfail(
    strict=True,
    reason="El dataset conserva una proporción controlada de diferencias.",
)
def test_refined_transactions_have_consistent_amounts(db_scalar):
    inconsistent_rows = db_scalar(
        """
        SELECT COUNT(*)
        FROM refinado.transacciones_refinado
        WHERE flag_inconsistencia_monto = 1
        """
    )
    assert inconsistent_rows == 0, (
        f"Se detectaron {inconsistent_rows} transacciones con monto inconsistente"
    )
