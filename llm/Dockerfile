FROM python:3.10-slim

# Instala pacotes essenciais
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    curl \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configura diretórios
WORKDIR /app
COPY requirements.txt .

# Cria diretório para modelos
RUN mkdir -p /app/models

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LLM_MODEL_PATH=/app/models/ggml-gpt4all-j-v1.3-groovy.bin \
    BACKEND_URL=http://backend:8000/api

# Instala dependências
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copia o código
COPY . .

# Baixa o modelo (opcional, comentado para o MVP por ser grande)
# Um modelo melhor seria baixá-lo como parte do script de inicialização
# RUN wget -O /app/models/ggml-gpt4all-j-v1.3-groovy.bin https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin

# Comando para iniciar o servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
