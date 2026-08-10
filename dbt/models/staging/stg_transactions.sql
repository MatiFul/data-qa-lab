select
    id_transaccion::integer as transaction_id,
    id_cuenta::integer as account_id,
    id_canal::integer as channel_id,
    id_estado::integer as status_id,
    id_sucursal::integer as branch_id,
    monto::numeric(12, 2) as transaction_amount,
    fecha_transaccion::timestamp as transaction_at,
    fecha_transaccion::date as transaction_date,
    fecha_proceso::date as processed_date
from {{ source('raw', 'transacciones_raw') }}
