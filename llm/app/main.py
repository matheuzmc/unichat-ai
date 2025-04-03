from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
from typing import Dict, List, Optional, Any
from .llm_service import generate_response, setup_llm
from .models import QueryRequest, QueryResponse, HealthCheckResponse

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="UniChat LLM Service",
    description="Serviço de processamento de linguagem natural para o UniChat",
    version="0.1.0"
)

# Configura o middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint de saúde
@app.get("/health", response_model=HealthCheckResponse)
def health_check():
    """Verifica se o serviço está operacional."""
    return HealthCheckResponse(status="ok", message="UniChat LLM Service is running")

# Endpoint raiz
@app.get("/")
def read_root():
    """Retorna informações básicas sobre o serviço."""
    return {"status": "ok", "message": "UniChat LLM Service is running"}

# Endpoint para processar consultas
@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Processa uma consulta do usuário.
    
    Esta função recebe uma pergunta e um ID de aluno, busca dados relevantes
    do backend e gera uma resposta contextualizada usando o LLM.
    """
    try:
        # Gera a resposta usando o serviço LLM
        answer = await generate_response(request.question, request.student_id, request.context_data)
        return QueryResponse(answer=answer)
    except Exception as e:
        # Loga o erro e retorna uma resposta de erro
        print(f"Erro ao processar consulta: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Inicialização do LLM ao iniciar o aplicativo
@app.on_event("startup")
async def startup_event():
    """Inicializa o modelo LLM quando o serviço é iniciado."""
    try:
        setup_llm()
        print("LLM inicializado com sucesso!")
    except Exception as e:
        print(f"Erro ao inicializar LLM: {str(e)}")
