import pytest


@pytest.mark.smoke
def test_database_connection(db_scalar):
    database_name = db_scalar("SELECT current_database()")
    assert database_name == "qa_lab"


@pytest.mark.smoke
def test_database_session_is_read_only(db_scalar):
    read_only_mode = db_scalar("SHOW default_transaction_read_only")
    assert read_only_mode == "on"


@pytest.mark.smoke
def test_required_schemas_exist(db_scalar):
    existing_schemas = db_scalar(
        """
        SELECT COUNT(*)
        FROM information_schema.schemata
        WHERE schema_name IN ('raw', 'curado', 'refinado', 'consumo')
        """
    )
    assert existing_schemas == 4


@pytest.mark.smoke
def test_core_tables_are_available(db_scalar):
    existing_tables = db_scalar(
        """
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema || '.' || table_name IN (
            'raw.transacciones_raw',
            'raw.items_transaccion_raw',
            'curado.transacciones_curado',
            'refinado.transacciones_refinado',
            'consumo.transacciones_consumo'
        )
        """
    )
    assert existing_tables == 5
