from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI(title="UniChat LLM Service")

class QueryRequest(BaseModel):
    question: str
    student_id: int

class QueryResponse(BaseModel):
    answer: str

# Uma função de resposta simulada para o MVP
# Em uma implementação real, aqui estaria a integração com um LLM via LangChain
def generate_response(question: str, student_id: int) -> str:
    return f"Esta é uma resposta simulada para a pergunta: '{question}' do aluno {student_id}. Em uma implementação real, esta resposta seria gerada por um LLM."

@app.get("/")
def read_root():
    return {"status": "ok", "message": "UniChat LLM Service is running"}

@app.post("/api/query", response_model=QueryResponse)
def process_query(request: QueryRequest):
    try:
        answer = generate_response(request.question, request.student_id)
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
