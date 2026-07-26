select
    transaction_date,
    count(*)::integer as transaction_count,
    sum(transaction_amount)::numeric(16, 2) as total_transaction_amount,
    sum(calculated_item_amount)::numeric(16, 2) as total_calculated_item_amount,
    sum(has_no_items_flag)::integer as transactions_without_items,
    sum(inconsistent_amount_flag)::integer as inconsistent_transactions,
    round(
        sum(inconsistent_amount_flag)::numeric / nullif(count(*), 0),
        4
    ) as inconsistency_rate
from {{ ref('fct_transaction_quality') }}
group by transaction_date
