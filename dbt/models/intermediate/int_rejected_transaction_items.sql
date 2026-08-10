select
    item.item_id,
    item.transaction_id,
    item.product_id,
    item.quantity,
    item.unit_price,
    item.item_amount,
    concat_ws(
        ',',
        case
            when source_transaction.transaction_id is null
                then 'unknown_transaction'
            when valid_transaction.transaction_id is null
                then 'rejected_transaction'
        end,
        case
            when product.product_id is null then 'unknown_product'
        end,
        case
            when item.quantity is null then 'null_quantity'
            when item.quantity <= 0 then 'non_positive_quantity'
        end,
        case
            when item.unit_price is null then 'null_unit_price'
            when item.unit_price <= 0 then 'non_positive_unit_price'
        end
    ) as rejection_reason
from {{ ref('stg_transaction_items') }} as item
left join {{ ref('stg_transactions') }} as source_transaction
    on item.transaction_id = source_transaction.transaction_id
left join {{ ref('int_valid_transactions') }} as valid_transaction
    on item.transaction_id = valid_transaction.transaction_id
left join {{ ref('stg_products') }} as product
    on item.product_id = product.product_id
where valid_transaction.transaction_id is null
   or product.product_id is null
   or item.quantity is null
   or item.quantity <= 0
   or item.unit_price is null
   or item.unit_price <= 0
