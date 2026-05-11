from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import json
import uuid
import time
from src.database.session import engine
from src.models.ml_model import PredictionLog
from sqlmodel import Session

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Captura erros de validação (Pydantic), sanitiza o payload e salva o log de erro no SQLite.
    """
    body = await request.body()
    try:
        payload_dict = json.loads(body.decode())
        # Sanitização: Removemos 'amount' do log de erro por questão de privacidade
        if "amount" in payload_dict:
            payload_dict["amount"] = "[REDACTED]"
        raw_payload = json.dumps(payload_dict)
    except Exception:
        raw_payload = "Unparsable Request Body"

    log = PredictionLog(
        transaction_id=str(uuid.uuid4()),
        status="VALIDATION_ERROR",
        error_message=str(exc.errors()),
        raw_payload=raw_payload,
        processing_time_ms=0.0  # Falhou antes de processar
    )

    with Session(engine) as session:
        session.add(log)
        session.commit()

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "message": "Validação falhou. Log registrado."}
    )