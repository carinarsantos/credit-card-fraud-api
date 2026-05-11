from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class PredictionLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    transaction_id: str = Field(index=True)
    status: str = Field(default="SUCCESS")
    prediction_score: Optional[float] = None
    is_fraud: Optional[bool] = None
    raw_payload: Optional[str] = Field(default=None, description="JSON bruto da transação")
    error_message: Optional[str] = None
    processing_time_ms: float
    created_at: datetime = Field(default_factory=datetime.utcnow)