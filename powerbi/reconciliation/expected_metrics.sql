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
from dbt_marts.fct_transaction_quality;

select
    sum(transaction_count)::integer as total_transactions,
    sum(inconsistent_transactions)::integer as inconsistent_transactions,
    sum(transactions_without_items)::integer as transactions_without_items,
    round(
        sum(inconsistent_transactions)::numeric
        / nullif(sum(transaction_count), 0),
        4
    ) as inconsistency_rate,
    min(transaction_date) as first_transaction_date,
    max(transaction_date) as last_transaction_date
from dbt_marts.mart_daily_quality;
