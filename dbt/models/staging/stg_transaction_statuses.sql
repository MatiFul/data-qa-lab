select
    id_estado::integer as status_id,
    descripcion_estado::text as status_description,
    es_final::integer as is_final
from {{ source('raw', 'estados_transaccion_raw') }}
