# 💳 Sistema de Detecção de Fraudes Bancárias

Este repositório contém uma solução ponta-a-ponta para detecção de fraudes em transações de cartão de crédito. O sistema utiliza Machine Learning para inferência em tempo real, exposto via uma API robusta e monitorado por um Dashboard interativo.

## 🚀 Destaques do Projeto
- **Interface em PT-BR:** Dashboard totalmente localizado para Português.
- **Simulador Inteligente:** Permite testar transações editando todas as 30 variáveis do modelo, incluindo um botão de carga para cenários reais de fraude.
- **Monitoramento Real-time:** Gráficos de latência, volume de requisições e taxa de detecção.
- **Data Drift:** Comparação estatística entre dados de produção e a baseline de treinamento.

## 🛠️ Estrutura Tecnológica
- **Backend:** FastAPI (Python 3.10) com SQLModel para persistência de logs.
- **Frontend:** Streamlit para o Dashboard de BI e simulação.
- **ML Model:** Scikit-Learn (Random Forest Classifier).
- **Infra:** Docker e Docker Compose para orquestração simplificada.

## ⚙️ Como Executar

### 1. Requisitos
- Docker e Docker Compose instalados.
- Dataset `creditcard.csv` na pasta `data/`.

### 2. Configuração e Treinamento
Caso queira gerar um novo modelo:
```bash
pip install -r requirements.txt
python src/train.py
```

### 3. Subindo o Sistema (Docker)
```bash
docker-compose up --build
```
- **API (Docs):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Dashboard:** [http://localhost:8501](http://localhost:8501)

## 📊 Notas para Recrutadores (Destaques Técnicos)

### Por que variáveis V1 a V28?
Os dados originais foram transformados via **PCA (Principal Component Analysis)** para garantir a privacidade dos clientes (conformidade com LGPD/GDPR). O modelo aprende padrões comportamentais nessas variáveis anonimizadas, o que é um cenário comum em grandes instituições financeiras.

### Tratamento de Desbalanceamento
O dataset é altamente desbalanceado (0,17% de fraudes). O modelo foi configurado com `class_weight='balanced'` e avaliado com métricas de precisão e sensibilidade (Recall) para garantir que as fraudes não passem despercebidas.

## 🔒 Segurança
A API exige o header `X-API-Key` para todos os endpoints sensíveis. Configure sua chave no arquivo `.env`.

---
*Desenvolvido como projeto de portfólio para Ciência de Dados e Engenharia de Machine Learning.*
