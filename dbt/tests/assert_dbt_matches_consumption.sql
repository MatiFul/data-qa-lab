with consumption as (
    select
        id_transaccion as transaction_id,
        monto_transaccion as transaction_amount,
        monto_calculado_items as calculated_item_amount,
        diferencia_monto as amount_difference,
        cantidad_items as item_count,
        flag_sin_items as has_no_items_flag,
        flag_inconsistencia_monto as inconsistent_amount_flag
    from consumo.transacciones_consumo
)

select
    coalesce(dbt.transaction_id, consumption.transaction_id) as transaction_id
from {{ ref('fct_transaction_quality') }} as dbt
full outer join consumption
    using (transaction_id)
where dbt.transaction_id is null
   or consumption.transaction_id is null
   or dbt.transaction_amount is distinct from consumption.transaction_amount
   or dbt.calculated_item_amount is distinct from
      consumption.calculated_item_amount
   or dbt.amount_difference is distinct from consumption.amount_difference
   or dbt.item_count is distinct from consumption.item_count
   or dbt.has_no_items_flag is distinct from consumption.has_no_items_flag
   or dbt.inconsistent_amount_flag is distinct from
      consumption.inconsistent_amount_flag
