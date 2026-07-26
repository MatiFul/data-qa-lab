from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    database: str


class QualitySummary(BaseModel):
    total_transactions: int
    inconsistent_transactions: int
    transactions_without_items: int
    inconsistency_rate: Decimal
    first_transaction_date: date | None
    last_transaction_date: date | None


class TransactionQuality(BaseModel):
    transaction_id: int
    account_id: int
    channel_id: int
    status_id: int
    branch_id: int
    transaction_amount: Decimal
    calculated_item_amount: Decimal
    amount_difference: Decimal
    item_count: int
    has_no_items_flag: int
    inconsistent_amount_flag: int
    transaction_at: datetime
    transaction_date: date
    processed_date: date


class TransactionList(BaseModel):
    count: int
    only_inconsistent: bool
    items: list[TransactionQuality]
