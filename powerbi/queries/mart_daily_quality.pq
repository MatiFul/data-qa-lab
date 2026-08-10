let
    Source = PostgreSQL.Database(
        "127.0.0.1:5434",
        "qa_lab",
        [
            Query = "
                select
                    transaction_date,
                    transaction_count,
                    total_transaction_amount,
                    total_calculated_item_amount,
                    transactions_without_items,
                    inconsistent_transactions,
                    inconsistency_rate
                from dbt_marts.mart_daily_quality
                order by transaction_date
            ",
            CommandTimeout = #duration(0, 0, 1, 0)
        ]
    )
in
    Source
