---
title: Credit Card Fraud API
emoji: 💳
colorFrom: blue
colorTo: red
sdk: docker
app_port: 7860
---

# Detecção de Fraudes em Cartões de Crédito
# Credit Card Fraud Detection: Full-Stack Data Solution


Este projeto implementa uma solução *end-to-end* para detecção de fraudes em transações de cartões de crédito. A arquitetura integra modelagem preditiva avançada e engenharia de software, disponibilizando a inferência via API REST e o monitoramento operacional através de um dashboard interativo.

## 🎯 Objetivo do Projeto

O foco é identificar transações fraudulentas em um conjunto de dados maciçamente desbalanceado (Dataset ULB - Université Libre de Bruxelles). A solução prioriza a **minimização de prejuízos financeiros reais**, ajustando de forma rigorosa o *trade-off* entre Sensibilidade (Recall) e Precisão, superando a visão limitante de apenas buscar alta "acurácia".

## 🏗️ Arquitetura do Sistema

A base do projeto segue os princípios de modularização e separação de responsabilidades (Microserviços):

*   **Modelo Preditivo:** Pipeline de pré-processamento, mitigação de desbalanceamento e treinamento refatorados de notebooks de pesquisa para scripts prontos para produção.
*   **FastAPI (Backend):** Motor de inferência robusto, assíncrono e tipado, que expõe o modelo via REST para integração com sistemas de autorização.
*   **Streamlit (Frontend):** Dashboard analítico para auditoria, exibindo métricas de performance (AUPRC), *Data Drift* e testes de inferência em tempo real.
*   **Pipeline de Qualidade:** Cobertura de testes unitários automatizados para garantir a estabilidade das transformações de dados e regras de roteamento.

## 💻 Tecnologias Utilizadas

*   **Linguagem Core:** `Python 3.10+`
*   **Ciência e Engenharia de Dados:** `Pandas`, `NumPy`, `Scikit-Learn`, `XGBoost/LightGBM`, `SMOTE` (Balanceamento).
*   **Web Services e API:** `FastAPI`, `Uvicorn`, `Pydantic` (Validação de Schemas).
*   **Frontend Analítico:** `Streamlit`, `Plotly`.
*   **Persistência e ORM:** `SQLite`, `SQLModel`.
*   **DevOps e Qualidade:** `Docker`, `Docker Compose`, `Pytest`.

## 📂 Estrutura do Repositório

```text
├── app/               # Interface frontend analítica (Streamlit)
├── src/               # Código-fonte backend (API, Serviços, Lógica de Banco)
├── notebooks/         # Ambiente de pesquisa, EDA e versionamento inicial de modelos
├── tests/             # Suíte de testes (Pytest)
├── models/            # (Ignorado no Git) Artefatos serializados (.joblib)
├── data/              # (Ignorado no Git) Banco SQLite persistente e datasets
└── docker-compose.yml # Orquestração da stack
```

## 🚀 Diferenciais Técnicos

Diferente de implementações acadêmicas de laboratório, este projeto foca em "Machine Learning Operacional":

1.  **Otimização por Custo Financeiro:** Avaliação do modelo orientada por uma *Matriz de Custo*, onde uma fraude não detectada (Falso Negativo) tem peso financeiro drasticamente diferente de um bloqueio preventivo errôneo (Falso Positivo).
2.  **Observabilidade e Resiliência:** Registro assíncrono de logs operacionais (latência, predições, status) e monitoramento de *Data Drift* contínuo.
3.  **Persistência via Volumes:** Uso estratégico do SQLite montado via volumes Docker para auditoria histórica sem dependência de nuvem.

---

## 🛠️ Como Executar o Projeto

A execução principal é orquestrada via Docker.

### 1. Início Rápido (Recomendado via Docker Compose)

Certifique-se de que o **Docker** e o **Docker Compose** estão instalados e rodando.

Na raiz do repositório, execute:
```bash
docker-compose up --build
```

**Acessos:**
*   **API (Backend):** [http://localhost:8000](http://localhost:8000) *(Documentação Swagger em `/docs`)*
*   **Dashboard (Frontend):** [http://localhost:8501](http://localhost:8501)

### 2. Execução Local (Desenvolvimento e Testes)

Caso queira rodar os testes unitários ou desenvolver localmente, configure o ambiente:

```bash
# 1. Clone o repositório
git clone https://github.com/carinarsantos/credit-card-fraud-api.git
cd credit-card-fraud-detection

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# No Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute a suíte de testes
pytest
```

## 🔒 Segurança e Persistência

*   **API Key:** Todas as requisições de predição exigem o header `X-API-Key`. Para desenvolvimento, a chave de segurança é injetada via variável de ambiente (definida no `.env` ou arquivo compose).
*   Persistência de Dados: Os logs operacionais e de predição são armazenados de forma persistente em ./data/fraud_logs.sqlite, preservando histórico entre reinicializações de contêineres.
