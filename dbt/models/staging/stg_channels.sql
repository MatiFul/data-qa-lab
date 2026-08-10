select
    id_canal::integer as channel_id,
    descripcion_canal::text as channel_description
from {{ source('raw', 'canales_raw') }}
