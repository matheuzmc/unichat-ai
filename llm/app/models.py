from pydantic import BaseModel
from typing import Dict, List, Optional, Any

class QueryRequest(BaseModel):
    """
    Modelo para a requisição de consulta ao LLM.
    
    Attributes:
        question: A pergunta feita pelo aluno.
        student_id: O ID do aluno que está fazendo a pergunta.
        context_data: Dados contextuais opcionais para enriquecer a resposta.
    """
    question: str
    student_id: int
    context_data: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    """
    Modelo para a resposta do LLM.
    
    Attributes:
        answer: A resposta gerada pelo LLM.
    """
    answer: str

class HealthCheckResponse(BaseModel):
    """
    Modelo para a resposta do endpoint de verificação de saúde.
    
    Attributes:
        status: O status atual do serviço (geralmente "ok").
        message: Uma mensagem descritiva sobre o estado do serviço.
    """
    status: str
    message: str 