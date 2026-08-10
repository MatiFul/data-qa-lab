select
    id_item::integer as item_id,
    id_transaccion::integer as transaction_id,
    id_producto::integer as product_id,
    cantidad::integer as quantity,
    precio_unitario::numeric(12, 2) as unit_price,
    (cantidad * precio_unitario)::numeric(14, 2) as item_amount
from {{ source('raw', 'items_transaccion_raw') }}
