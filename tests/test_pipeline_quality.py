import pytest


@pytest.mark.quality
def test_transaction_flow_is_reconciled(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM raw.transacciones_raw),
                (SELECT COUNT(*) FROM dbt_staging.stg_transactions),
                (SELECT COUNT(*) FROM dbt_intermediate.int_valid_transactions),
                (SELECT COUNT(*) FROM dbt_intermediate.int_rejected_transactions),
                (SELECT COUNT(*) FROM dbt_marts.fct_transaction_quality)
            """
        )
        raw, staging, valid, rejected, mart = cursor.fetchone()

    assert raw == staging
    assert staging == valid + rejected
    assert valid == mart
    assert valid > 0
    assert rejected > 0


@pytest.mark.quality
def test_item_flow_is_reconciled(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM raw.items_transaccion_raw),
                (SELECT COUNT(*) FROM dbt_staging.stg_transaction_items),
                (
                    SELECT COUNT(*)
                    FROM dbt_intermediate.int_valid_transaction_items
                ),
                (
                    SELECT COUNT(*)
                    FROM dbt_intermediate.int_rejected_transaction_items
                )
            """
        )
        raw, staging, valid, rejected = cursor.fetchone()

    assert raw == staging
    assert staging == valid + rejected
    assert valid > 0


@pytest.mark.quality
@pytest.mark.parametrize(
    "relation",
    [
        "dbt_intermediate.int_rejected_transactions",
        "dbt_intermediate.int_rejected_transaction_items",
    ],
)
def test_rejected_rows_have_a_reason(db_scalar, relation):
    rejected_without_reason = db_scalar(
        f"""
        SELECT COUNT(*)
        FROM {relation}
        WHERE rejection_reason IS NULL
           OR rejection_reason = ''
        """
    )
    assert rejected_without_reason == 0


@pytest.mark.quality
def test_consumer_mart_contains_only_valid_transactions(db_scalar):
    inconsistent_keys = db_scalar(
        """
        SELECT COUNT(*)
        FROM dbt_marts.fct_transaction_quality mart
        FULL OUTER JOIN dbt_intermediate.int_valid_transactions intermediate
          USING (transaction_id)
        WHERE mart.transaction_id IS NULL
           OR intermediate.transaction_id IS NULL
        """
    )
    assert inconsistent_keys == 0


@pytest.mark.quality
def test_daily_mart_reconciles_with_transaction_mart(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM dbt_marts.fct_transaction_quality),
                (
                    SELECT COALESCE(SUM(transaction_count), 0)
                    FROM dbt_marts.mart_daily_quality
                ),
                (
                    SELECT COALESCE(SUM(transaction_amount), 0)
                    FROM dbt_marts.fct_transaction_quality
                ),
                (
                    SELECT COALESCE(SUM(total_transaction_amount), 0)
                    FROM dbt_marts.mart_daily_quality
                )
            """
        )
        fact_rows, daily_rows, fact_amount, daily_amount = cursor.fetchone()

    assert fact_rows == daily_rows
    assert fact_amount == daily_amount
