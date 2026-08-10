with partitioned as (
    select item_id
    from {{ ref('int_valid_transaction_items') }}

    union all

    select item_id
    from {{ ref('int_rejected_transaction_items') }}
),

membership as (
    select
        item_id,
        count(*) as membership_count
    from partitioned
    group by item_id
)

select staging.item_id
from {{ ref('stg_transaction_items') }} as staging
left join membership
    on staging.item_id = membership.item_id
where coalesce(membership.membership_count, 0) != 1

union all

select membership.item_id
from membership
left join {{ ref('stg_transaction_items') }} as staging
    on membership.item_id = staging.item_id
where staging.item_id is null
