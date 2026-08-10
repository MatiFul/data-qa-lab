select
    transaction.transaction_id,
    transaction.account_id,
    transaction.channel_id,
    transaction.status_id,
    transaction.branch_id,
    transaction.transaction_amount,
    transaction.transaction_at,
    transaction.transaction_date,
    transaction.processed_date,
    concat_ws(
        ',',
        case
            when transaction.transaction_amount is null then 'null_amount'
        end,
        case
            when transaction.transaction_amount < 0 then 'negative_amount'
        end,
        case
            when transaction.transaction_at is null then 'null_transaction_date'
        end,
        case
            when transaction.processed_date is null then 'null_processed_date'
        end,
        case
            when account.account_id is null then 'unknown_account'
        end,
        case
            when channel.channel_id is null then 'unknown_channel'
        end,
        case
            when status.status_id is null then 'unknown_status'
        end
    ) as rejection_reason
from {{ ref('stg_transactions') }} as transaction
left join {{ ref('stg_accounts') }} as account
    on transaction.account_id = account.account_id
left join {{ ref('stg_channels') }} as channel
    on transaction.channel_id = channel.channel_id
left join {{ ref('stg_transaction_statuses') }} as status
    on transaction.status_id = status.status_id
where transaction.transaction_amount is null
   or transaction.transaction_amount < 0
   or transaction.transaction_at is null
   or transaction.processed_date is null
   or account.account_id is null
   or channel.channel_id is null
   or status.status_id is null
