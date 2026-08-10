select
    id_cuenta::integer as account_id,
    id_cliente::integer as customer_id,
    tipo_cuenta::text as account_type,
    estado_cuenta::text as account_status,
    fecha_alta::date as opened_date
from {{ source('raw', 'cuentas_raw') }}
