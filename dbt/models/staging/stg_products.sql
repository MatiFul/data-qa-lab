select
    id_producto::integer as product_id,
    nombre_producto::text as product_name,
    categoria::text as category,
    activo::integer as is_active
from {{ source('raw', 'productos_raw') }}
