# Usa uma imagem oficial do Python, versão slim para reduzir o tamanho
FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema necessárias para compilar bibliotecas C (como NumPy/Pandas)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências do Python primeiro (aproveita cache de build do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Expõe as portas (documentação)
EXPOSE 8000 8501

# Comando de inicialização padrão (usado pelo Hugging Face Spaces na porta 7860)
CMD ["uvicorn", "src.api.routes:app", "--host", "0.0.0.0", "--port", "7860"]