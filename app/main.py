from pathlib import Path

import psycopg
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.database import read_only_connection
from app.models import (
    HealthResponse,
    QualitySummary,
    TransactionList,
    TransactionQuality,
)

STATIC_DIRECTORY = Path(__file__).resolve().parent / "static"

app = FastAPI(
    title="Data QA Lab API",
    description="API de sólo lectura para practicar QA de API, web y datos.",
    version="2.0.0",
)
app.mount("/static", StaticFiles(directory=STATIC_DIRECTORY), name="static")


@app.get("/", include_in_schema=False)
def dashboard() -> FileResponse:
    return FileResponse(STATIC_DIRECTORY / "index.html")


@app.get("/health", response_model=HealthResponse, tags=["operación"])
def health() -> HealthResponse:
    try:
        with read_only_connection() as connection:
            connection.execute("select 1")
    except (psycopg.Error, RuntimeError) as error:
        raise HTTPException(
            status_code=503,
            detail="La API no puede consultar PostgreSQL.",
        ) from error

    return HealthResponse(status="ok", database="connected")


@app.get(
    "/api/quality/summary",
    response_model=QualitySummary,
    tags=["calidad"],
)
def quality_summary() -> QualitySummary:
    query = """
        select
            count(*)::integer as total_transactions,
            coalesce(sum(inconsistent_amount_flag), 0)::integer
                as inconsistent_transactions,
            coalesce(sum(has_no_items_flag), 0)::integer
                as transactions_without_items,
            round(
                coalesce(sum(inconsistent_amount_flag), 0)::numeric
                / nullif(count(*), 0),
                4
            ) as inconsistency_rate,
            min(transaction_date) as first_transaction_date,
            max(transaction_date) as last_transaction_date
        from dbt_marts.fct_transaction_quality
    """
    try:
        with read_only_connection() as connection:
            row = connection.execute(query).fetchone()
    except (psycopg.Error, RuntimeError) as error:
        raise HTTPException(
            status_code=503,
            detail="No fue posible calcular el resumen de calidad.",
        ) from error

    if row is None or row["total_transactions"] == 0:
        raise HTTPException(status_code=404, detail="No hay datos para resumir.")
    return QualitySummary.model_validate(row)


@app.get(
    "/api/transactions",
    response_model=TransactionList,
    tags=["transacciones"],
)
def list_transactions(
    only_inconsistent: bool = False,
    limit: int = Query(default=20, ge=1, le=100),
) -> TransactionList:
    where_clause = "where inconsistent_amount_flag = 1" if only_inconsistent else ""
    query = f"""
        select
            transaction_id,
            account_id,
            channel_id,
            status_id,
            branch_id,
            transaction_amount,
            calculated_item_amount,
            amount_difference,
            item_count,
            has_no_items_flag,
            inconsistent_amount_flag,
            transaction_at,
            transaction_date,
            processed_date
        from dbt_marts.fct_transaction_quality
        {where_clause}
        order by transaction_id
        limit %s
    """
    try:
        with read_only_connection() as connection:
            rows = connection.execute(query, (limit,)).fetchall()
    except (psycopg.Error, RuntimeError) as error:
        raise HTTPException(
            status_code=503,
            detail="No fue posible consultar las transacciones.",
        ) from error

    items = [TransactionQuality.model_validate(row) for row in rows]
    return TransactionList(
        count=len(items),
        only_inconsistent=only_inconsistent,
        items=items,
    )


@app.get(
    "/api/transactions/{transaction_id}",
    response_model=TransactionQuality,
    tags=["transacciones"],
)
def transaction_detail(transaction_id: int) -> TransactionQuality:
    query = """
        select
            transaction_id,
            account_id,
            channel_id,
            status_id,
            branch_id,
            transaction_amount,
            calculated_item_amount,
            amount_difference,
            item_count,
            has_no_items_flag,
            inconsistent_amount_flag,
            transaction_at,
            transaction_date,
            processed_date
        from dbt_marts.fct_transaction_quality
        where transaction_id = %s
    """
    try:
        with read_only_connection() as connection:
            row = connection.execute(query, (transaction_id,)).fetchone()
    except (psycopg.Error, RuntimeError) as error:
        raise HTTPException(
            status_code=503,
            detail="No fue posible consultar la transacción.",
        ) from error

    if row is None:
        raise HTTPException(status_code=404, detail="Transacción no encontrada.")
    return TransactionQuality.model_validate(row)
