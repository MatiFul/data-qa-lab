select
    item.item_id,
    item.transaction_id,
    item.product_id,
    item.quantity,
    item.unit_price,
    item.item_amount
from {{ ref('stg_transaction_items') }} as item
inner join {{ ref('int_valid_transactions') }} as transaction
    on item.transaction_id = transaction.transaction_id
inner join {{ ref('stg_products') }} as product
    on item.product_id = product.product_id
where item.quantity is not null
  and item.quantity > 0
  and item.unit_price is not null
  and item.unit_price > 0
