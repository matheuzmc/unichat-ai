FROM python:3.10-slim

# Instala pacotes essenciais
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    curl \
    wget \
    git \
    cmake \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configura diretórios
WORKDIR /app
COPY requirements.txt .

# Cria diretório para modelos com permissões adequadas
RUN mkdir -p /app/models && chmod 777 /app/models

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LLM_MODEL_PATH=/app/models/Phi-3-mini-4k-instruct-q4.gguf \
    BACKEND_URL=http://backend:8000/api

# Instala dependências
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Instala llama-cpp-python com suporte a CPU
RUN pip install llama-cpp-python

# Copia o código
COPY . .

# Comando para iniciar o servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
