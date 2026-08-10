let
    Source = PostgreSQL.Database(
        "127.0.0.1:5434",
        "qa_lab",
        [
            Query = "
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
            ",
            CommandTimeout = #duration(0, 0, 1, 0)
        ]
    )
in
    Source
