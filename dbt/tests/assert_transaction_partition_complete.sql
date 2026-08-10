with partitioned as (
    select transaction_id
    from {{ ref('int_valid_transactions') }}

    union all

    select transaction_id
    from {{ ref('int_rejected_transactions') }}
),

membership as (
    select
        transaction_id,
        count(*) as membership_count
    from partitioned
    group by transaction_id
)

select staging.transaction_id
from {{ ref('stg_transactions') }} as staging
left join membership
    on staging.transaction_id = membership.transaction_id
where coalesce(membership.membership_count, 0) != 1

union all

select membership.transaction_id
from membership
left join {{ ref('stg_transactions') }} as staging
    on membership.transaction_id = staging.transaction_id
where staging.transaction_id is null
