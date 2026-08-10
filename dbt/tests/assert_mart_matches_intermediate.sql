select
    coalesce(mart.transaction_id, intermediate.transaction_id) as transaction_id
from {{ ref('fct_transaction_quality') }} as mart
full outer join {{ ref('int_valid_transactions') }} as intermediate
    using (transaction_id)
where mart.transaction_id is null
   or intermediate.transaction_id is null
   or mart.transaction_amount is distinct from intermediate.transaction_amount
   or mart.transaction_at is distinct from intermediate.transaction_at
   or mart.processed_date is distinct from intermediate.processed_date
