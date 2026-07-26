select *
from {{ ref('fct_transaction_quality') }}
where has_no_items_flag is distinct from
      case when item_count = 0 then 1 else 0 end
   or inconsistent_amount_flag is distinct from
      case when abs(amount_difference) > 1 then 1 else 0 end
