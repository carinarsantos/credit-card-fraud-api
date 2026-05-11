import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from sqlmodel import select

from src.api.routes import app, get_session, predictor
from src.database.session import engine

# Configuração do Banco em Memória para Testes
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", 
        connect_args={"check_same_thread": False}, 
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

# Mock do Preditor para evitar carregar o .joblib real
class MockPredictor:
    def predict(self, features):
        return False, 0.01  # Retorna sempre 'Não Fraude' com 1% de prob

@pytest.fixture(autouse=True)
def mock_ml_model(monkeypatch):
    # Substitui o carregamento do modelo real pelo mock
    monkeypatch.setattr(predictor, "model", MockPredictor())
    monkeypatch.setattr(predictor, "load_model", lambda: None)

# --- TESTES ---

def test_predict_without_api_key(client: TestClient):
    """Garante que a API bloqueia acesso sem a chave."""
    response = client.post("/v1/predict", json={"time": 0, "amount": 100})
    assert response.status_code == 403

def test_predict_invalid_data(client: TestClient):
    """Valida se o Pydantic bloqueia dados corrompidos/incompletos."""
    headers = {"X-API-Key": "chave-secreta-padrao"}
    # Enviando apenas 2 campos em vez dos 30 esperados
    response = client.post("/v1/predict", headers=headers, json={"v1": 0.5, "amount": 10})
    assert response.status_code == 422

def test_predict_success_and_db_persistence(client: TestClient, session: Session):
    headers = {"X-API-Key": "chave-secreta-padrao"}
    payload = {f"v{i}": 0.0 for i in range(1, 29)}
    payload.update({"time": 0.0, "amount": 100.0})
    
    # Executa a chamada
    response = client.post("/v1/predict?sensitivity=0.3", headers=headers, json=payload)
    assert response.status_code == 200

    data = response.json()
    transaction_id = data["transaction_id"]
    
    # Consulta direta no banco de dados in-memory para validar a persistência
    statement = select(PredictionLog).where(PredictionLog.transaction_id == transaction_id)
    log_entry = session.exec(statement).first()
    
    assert log_entry is not None
    assert log_entry.status == "SUCCESS"
    assert log_entry.prediction_score is not None
    assert log_entry.raw_payload is None # No sucesso configuramos para não salvar