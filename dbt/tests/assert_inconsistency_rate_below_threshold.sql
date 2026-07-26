with quality_rate as (
    select
        count(*) filter (where inconsistent_amount_flag = 1)::numeric
            / nullif(count(*), 0) as inconsistency_rate
    from {{ ref('fct_transaction_quality') }}
)

select *
from quality_rate
where inconsistency_rate > {{ var('max_inconsistency_rate', 0.05) }}
