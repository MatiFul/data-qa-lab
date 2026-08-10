select
    transaction_id,
    count(item_id)::integer as item_count,
    sum(item_amount)::numeric(14, 2) as calculated_item_amount
from {{ ref('int_valid_transaction_items') }}
group by transaction_id
