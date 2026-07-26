with item_totals as (
    select
        transaction_id,
        count(item_id)::integer as item_count,
        sum(item_amount)::numeric(14, 2) as calculated_item_amount
    from {{ ref('stg_transaction_items') }}
    group by transaction_id
)

select
    transaction.transaction_id,
    transaction.account_id,
    transaction.channel_id,
    transaction.status_id,
    transaction.branch_id,
    transaction.transaction_amount,
    coalesce(item.calculated_item_amount, 0)::numeric(14, 2)
        as calculated_item_amount,
    (
        transaction.transaction_amount
        - coalesce(item.calculated_item_amount, 0)
    )::numeric(14, 2) as amount_difference,
    coalesce(item.item_count, 0)::integer as item_count,
    case
        when coalesce(item.item_count, 0) = 0 then 1
        else 0
    end::integer as has_no_items_flag,
    case
        when abs(
            transaction.transaction_amount
            - coalesce(item.calculated_item_amount, 0)
        ) > 1 then 1
        else 0
    end::integer as inconsistent_amount_flag,
    transaction.transaction_at,
    transaction.transaction_date,
    transaction.processed_date,
    current_timestamp as dbt_loaded_at
from {{ ref('stg_transactions') }} as transaction
left join item_totals as item
    on transaction.transaction_id = item.transaction_id
