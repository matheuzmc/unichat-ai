import os
from typing import Dict, List, Optional, Any
import requests
from langchain.llms import GPT4All
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Variáveis globais
llm = None
backend_url = os.getenv("BACKEND_URL", "http://backend:8000/api")
model_path = os.getenv("LLM_MODEL_PATH", "/app/models/model.bin")

def setup_llm():
    """
    Configura e inicializa o modelo LLM.
    
    Esta função configura o modelo GPT4All usando o arquivo especificado
    em LLM_MODEL_PATH ou usa um caminho padrão.
    """
    global llm
    
    # Verifica se o modelo existe, se não, usa uma simulação
    if os.path.exists(model_path):
        # Em um ambiente real, carregar o modelo GPT4All
        try:
            llm = GPT4All(model=model_path, verbose=True)
            print(f"Modelo GPT4All carregado do caminho: {model_path}")
        except Exception as e:
            print(f"Erro ao carregar modelo GPT4All: {str(e)}")
            # Fallback: usar um LLM simulado
            llm = None
    else:
        print(f"Arquivo de modelo não encontrado em {model_path}. Usando LLM simulado.")
        llm = None

async def fetch_student_data(student_id: int) -> Dict[str, Any]:
    """
    Busca dados do aluno no backend.
    
    Args:
        student_id: O ID do aluno para buscar os dados.
        
    Returns:
        Um dicionário com os dados do aluno.
    """
    try:
        # Busca detalhes do aluno
        response = requests.get(f"{backend_url}/alunos/{student_id}/detalhes/")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro ao buscar dados do aluno: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Exceção ao buscar dados do aluno: {str(e)}")
        return {}

def create_system_prompt(student_data: Dict[str, Any]) -> str:
    """
    Cria um prompt de sistema com informações relevantes do aluno.
    
    Args:
        student_data: Dados do aluno a serem incluídos no prompt.
        
    Returns:
        Um prompt formatado com informações do aluno.
    """
    # Extrai informações relevantes dos dados do aluno
    if not student_data:
        return """
        Você é um assistente acadêmico chamado UniChat. Você ajuda alunos com informações
        sobre suas notas, horários, finanças e outros aspectos acadêmicos. 
        Seja cordial e direto nas respostas. Se não tiver informações suficientes,
        peça mais detalhes ou sugira que o aluno entre em contato com a coordenação.
        """
    
    # Extrai nome e dados básicos
    nome = student_data.get("nome", "Aluno")
    curso = student_data.get("curso", "")
    semestre = student_data.get("semestre", "")
    
    # Formata notas (se disponíveis)
    notas_info = ""
    if "notas" in student_data and student_data["notas"]:
        notas_info = "Notas do aluno:\n"
        for nota in student_data["notas"][:5]:  # Limita a 5 notas para o prompt
            notas_info += f"- {nota.get('disciplina')}: {nota.get('nota_final')}\n"
    
    # Formata horários (se disponíveis)
    horarios_info = ""
    if "horarios" in student_data and student_data["horarios"]:
        horarios_info = "Horários de aula:\n"
        for horario in student_data["horarios"][:5]:  # Limita a 5 horários
            horarios_info += f"- {horario.get('disciplina')}: {horario.get('dia_semana_display')} {horario.get('horario_inicio')} - {horario.get('horario_fim')}\n"
    
    # Constrói o prompt completo
    prompt = f"""
    Você é um assistente acadêmico chamado UniChat que está ajudando {nome}.
    
    Informações do aluno:
    - Nome: {nome}
    - Curso: {curso}
    - Semestre: {semestre}
    
    {notas_info}
    
    {horarios_info}
    
    Seja cordial e direto nas respostas. Use as informações acima para contextualizar suas respostas.
    Se não tiver informações suficientes, peça mais detalhes ou sugira que o aluno entre em contato com a coordenação.
    """
    
    return prompt

async def generate_response(question: str, student_id: int, context_data: Optional[Dict[str, Any]] = None) -> str:
    """
    Gera uma resposta para a pergunta do aluno.
    
    Args:
        question: A pergunta feita pelo aluno.
        student_id: O ID do aluno para contextualizar a resposta.
        context_data: Dados de contexto adicionais (opcional).
        
    Returns:
        A resposta gerada pelo LLM.
    """
    # Busca dados do aluno (se não fornecidos no context_data)
    student_data = context_data or await fetch_student_data(student_id)
    
    # Cria um prompt de sistema
    system_prompt = create_system_prompt(student_data)
    
    # Prepara o prompt completo
    prompt_template = f"{system_prompt}\n\nPergunta: {question}\n\nResposta:"
    
    # Verifica se o LLM está disponível
    if llm:
        try:
            # Gera a resposta usando o LLM real
            response = llm(prompt_template)
            return response.strip()
        except Exception as e:
            print(f"Erro ao gerar resposta com LLM: {str(e)}")
            # Fallback para resposta simulada
            return simulate_response(question, student_data)
    else:
        # Usa uma resposta simulada se o LLM não estiver disponível
        return simulate_response(question, student_data)

def simulate_response(question: str, student_data: Dict[str, Any]) -> str:
    """
    Gera uma resposta simulada quando o LLM não está disponível.
    
    Args:
        question: A pergunta feita pelo aluno.
        student_data: Dados do aluno para contextualizar a resposta.
        
    Returns:
        Uma resposta simulada baseada em regras.
    """
    question_lower = question.lower()
    nome = student_data.get("nome", "Aluno") if student_data else "Aluno"
    
    # Responde com base em palavras-chave na pergunta
    if "nota" in question_lower or "avaliação" in question_lower or "prova" in question_lower:
        # Resposta sobre notas
        if student_data and "notas" in student_data and student_data["notas"]:
            disciplina = next((nota["disciplina"] for nota in student_data["notas"] if nota["disciplina"].lower() in question_lower), None)
            if disciplina:
                nota = next((nota for nota in student_data["notas"] if nota["disciplina"] == disciplina), None)
                if nota:
                    return f"Olá {nome}! Sua nota em {disciplina} é {nota['nota_final']}."
            
            return f"Olá {nome}! Você tem as seguintes notas registradas: " + ", ".join([f"{nota['disciplina']}: {nota['nota_final']}" for nota in student_data["notas"][:3]])
        return f"Olá {nome}! Não encontrei informações sobre suas notas no sistema. Entre em contato com a secretaria para mais detalhes."
    
    elif "horário" in question_lower or "aula" in question_lower or "disciplina" in question_lower:
        # Resposta sobre horários
        if student_data and "horarios" in student_data and student_data["horarios"]:
            disciplina = next((horario["disciplina"] for horario in student_data["horarios"] if horario["disciplina"].lower() in question_lower), None)
            if disciplina:
                horario = next((horario for horario in student_data["horarios"] if horario["disciplina"] == disciplina), None)
                if horario:
                    return f"Olá {nome}! Sua aula de {disciplina} é {horario['dia_semana_display']} das {horario['horario_inicio']} às {horario['horario_fim']} na sala {horario['sala']}."
            
            return f"Olá {nome}! Seus horários de aula são: " + "; ".join([f"{horario['disciplina']}: {horario['dia_semana_display']} {horario['horario_inicio']}-{horario['horario_fim']}" for horario in student_data["horarios"][:3]])
        return f"Olá {nome}! Não encontrei informações sobre seus horários no sistema. Verifique com a coordenação."
    
    elif "mensalidade" in question_lower or "financeiro" in question_lower or "pagamento" in question_lower:
        # Resposta sobre dados financeiros
        if student_data and "dados_financeiros" in student_data and student_data["dados_financeiros"]:
            dados = student_data["dados_financeiros"][0]  # Pega o primeiro registro
            return f"Olá {nome}! Sua próxima mensalidade no valor de R${dados['mensalidade']} vence em {dados['data_vencimento']} e está com status {dados['status_pagamento_display']}."
        return f"Olá {nome}! Não encontrei informações financeiras no sistema. Entre em contato com o setor financeiro."
    
    # Resposta genérica
    return f"Olá {nome}! Entendi sua pergunta sobre '{question}'. Como posso ajudar com mais detalhes? Você pode perguntar sobre notas, horários, mensalidades ou outros assuntos acadêmicos." 