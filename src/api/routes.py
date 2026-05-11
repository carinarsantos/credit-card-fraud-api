import time
import uuid
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, APIRouter, Depends, BackgroundTasks, HTTPException, status
from sqlmodel import Session, select

from src.database.session import engine, get_session, create_db_and_tables
from src.models.ml_model import PredictionLog
from src.api.schemas import TransactionInput
from src.api.security import get_api_key
from src.services.predictor import FraudPredictor
from src.api.handlers import validation_exception_handler
from fastapi.exceptions import RequestValidationError

# Singleton do preditor
predictor = FraudPredictor(model_path="artifacts/fraud_model.joblib")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup inicial: tabelas e carregamento do modelo
    create_db_and_tables()
    predictor.load_model()
    yield

app = FastAPI(
    title="Fraud Detection API",
    description="API para detecção de fraudes em tempo real.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)

router_v1 = APIRouter(prefix="/v1", tags=["v1"])

def log_prediction_to_db(log_data: PredictionLog):
    """Persistência assíncrona de logs no banco."""
    with Session(engine) as session:
        session.add(log_data)
        session.commit()

@router_v1.get("/logs", dependencies=[Depends(get_api_key)])
async def get_prediction_logs(
    limit: int = 100,
    db: Session = Depends(get_session)
):
    """Retorna histórico de predições."""
    statement = select(PredictionLog).order_by(PredictionLog.created_at.desc()).limit(limit)
    logs = db.exec(statement).all()
    return [log.model_dump() for log in logs]

@router_v1.post("/predict", status_code=status.HTTP_200_OK)
async def predict_v1(
    data: TransactionInput, 
    background_tasks: BackgroundTasks,
    sensitivity: float = 0.5,
    api_key: str = Depends(get_api_key)
):
    """Executa a predição de fraude para uma transação."""
    start_time = time.perf_counter()
    transaction_id = str(uuid.uuid4())
    
    try:
        payload_dict = data.model_dump()
        is_fraud, probability = predictor.predict(payload_dict, threshold=sensitivity)
        
        duration = (time.perf_counter() - start_time) * 1000
        
        log = PredictionLog(
            transaction_id=transaction_id,
            prediction_score=probability,
            is_fraud=is_fraud,
            raw_payload=data.model_dump_json(),
            processing_time_ms=duration,
            status="SUCCESS"
        )
        background_tasks.add_task(log_prediction_to_db, log)
        
        return {
            "transaction_id": transaction_id, 
            "is_fraud": is_fraud, 
            "probability": round(probability, 4)
        }

    except Exception as e:
        duration = (time.perf_counter() - start_time) * 1000
        log = PredictionLog(
            transaction_id=transaction_id,
            status="FAILED",
            error_message=str(e),
            raw_payload=data.model_dump_json(),
            processing_time_ms=duration
        )
        background_tasks.add_task(log_prediction_to_db, log)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Erro no processamento: {str(e)}"
        )

app.include_router(router_v1)