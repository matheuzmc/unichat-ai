#!/bin/bash
set -e

# Verifica se o modelo existe
MODEL_PATH=${LLM_MODEL_PATH:-/app/models/Phi-3-mini-4k-instruct-q4.gguf}
if [ ! -f "$MODEL_PATH" ]; then
    echo "AVISO: Modelo não encontrado em $MODEL_PATH"
    echo "Certifique-se de que o modelo foi copiado corretamente para o volume de modelos"
fi

# Inicia o servidor
exec uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload "$@" 