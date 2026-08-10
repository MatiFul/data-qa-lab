select
    transaction.transaction_id,
    transaction.account_id,
    transaction.channel_id,
    transaction.status_id,
    transaction.branch_id,
    transaction.transaction_amount,
    transaction.transaction_at,
    transaction.transaction_date,
    transaction.processed_date
from {{ ref('stg_transactions') }} as transaction
inner join {{ ref('stg_accounts') }} as account
    on transaction.account_id = account.account_id
inner join {{ ref('stg_channels') }} as channel
    on transaction.channel_id = channel.channel_id
inner join {{ ref('stg_transaction_statuses') }} as status
    on transaction.status_id = status.status_id
where transaction.transaction_amount is not null
  and transaction.transaction_amount >= 0
  and transaction.transaction_at is not null
  and transaction.processed_date is not null
