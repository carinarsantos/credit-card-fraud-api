import os
from sqlmodel import SQLModel, create_engine, Session

# Pega o caminho do banco das variáveis de ambiente (com fallback para local)
SQLITE_URL = os.getenv("DATABASE_URL", "sqlite:///./fraud_logs.sqlite")

engine = create_engine(
    SQLITE_URL, 
    echo=False, # Não poluir os logs de produção
    connect_args={"check_same_thread": False} # Necessário para FastAPI + SQLite
)

def create_db_and_tables():
    """Cria as tabelas caso não existam."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Gera sessões para injeção de dependência no FastAPI."""
    with Session(engine) as session:
        yield session