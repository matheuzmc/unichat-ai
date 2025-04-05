import sys
import os
from typing import Dict, List, Optional, Any
import requests
import json
import random
import time
import logging
import urllib.request
import shutil
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import gc
import time
from threading import Thread

# Import da configuração da plataforma
from .platform_config import get_model_config, should_run_gc, is_mac_m1

# Configurar logging com rotação de arquivos
try:
    from logging.handlers import RotatingFileHandler
    log_handler = RotatingFileHandler("llm_service.log", maxBytes=1024*1024*5, backupCount=3)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[log_handler, logging.StreamHandler()]
    )
except:
    # Fallback para configuração padrão
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

# Importação para o modelo GPT4All
try:
    from langchain.llms import GPT4All
    has_gpt4all = True
except Exception as e:
    logger.error(f"Erro ao importar GPT4All: {e}")
    has_gpt4all = False

# Importação para o modelo GGUF
try:
    import llama_cpp
    has_llama_cpp = True
    logger.info("llama-cpp-python importado com sucesso!")
    logger.info(f"Caminho do módulo llama_cpp: {llama_cpp.__file__}")
except ImportError as e:
    logger.warning(f"llama-cpp-python não está disponível. O modelo GGUF não será utilizado. Erro: {e}")
    has_llama_cpp = False

# Carrega variáveis de ambiente
load_dotenv()

# Variáveis globais
llm = None
llm_gguf = None  # Modelo GGUF
cleanup_thread = None
backend_url = os.getenv("BACKEND_URL", "http://backend/api")
model_path = os.getenv("LLM_MODEL_PATH", "/app/models/Phi-3-mini-4k-instruct-q4.gguf")
# URL atualizada para um modelo no Hugging Face
model_url = os.getenv("LLM_MODEL_URL", "https://huggingface.co/mradermacher/ggml-gpt4all-j-v1.3-groovy/resolve/main/ggml-gpt4all-j-v1.3-groovy.bin")

def memory_cleanup():
    """Executa limpeza de memória periódica."""
    interval = get_model_config().get("gc_interval", 60)
    logger.info(f"Iniciando thread de limpeza de memória a cada {interval} segundos")
    
    while True:
        time.sleep(interval)
        before = get_memory_usage()
        gc.collect()
        after = get_memory_usage()
        logger.info(f"Limpeza de memória executada. Antes: {before}MB, Depois: {after}MB, Liberado: {max(0, before - after):.2f}MB")

def get_memory_usage():
    """Retorna o uso de memória atual em MB."""
    try:
        import psutil
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024
    except ImportError:
        return 0

def start_gc_thread():
    """Inicia o thread de limpeza de memória."""
    global cleanup_thread
    if cleanup_thread is None:
        cleanup_thread = Thread(target=memory_cleanup, daemon=True)
        cleanup_thread.start()
        logger.info("Thread de limpeza de memória iniciado")

def setup_llm():
    """
    Configura e inicializa o modelo LLM.
    
    Esta função tenta carregar primeiramente o modelo GGUF. Se não for possível,
    tenta carregar o modelo GPT4All. Se ambos falharem, usa simulação.
    """
    global llm, llm_gguf
    
    # Verifica se o modelo existe
    if not os.path.exists(model_path):
        logger.info(f"Modelo não encontrado em {model_path}.")
        logger.warning("O modelo precisa ser baixado manualmente. Usando LLM simulado.")
        logger.info(f"Para usar o LLM real, baixe o modelo de {model_url} e coloque-o em {model_path}")
        llm = None
        llm_gguf = None
        return
    
    # Verifica a extensão do arquivo para determinar o tipo de modelo
    is_gguf = model_path.endswith('.gguf')
    logger.info(f"Verificando modelo: {model_path}, é GGUF: {is_gguf}, has_llama_cpp: {has_llama_cpp}")
    
    if is_gguf and has_llama_cpp:
        try:
            # Obter configurações para a plataforma atual
            config = get_model_config("gguf")
            logger.info(f"Usando configuração para a plataforma: {config}")
            
            # Tentar carregar o modelo GGUF com llama-cpp-python
            logger.info(f"Tentando carregar modelo GGUF de {model_path}...")
            
            # Usar a configuração da plataforma
            llm_gguf = llama_cpp.Llama(
                model_path=model_path,
                n_ctx=config.get("n_ctx", 4096),
                n_batch=config.get("n_batch", 512),
                n_threads=config.get("n_threads", 4),
                n_gpu_layers=config.get("n_gpu_layers", 40),
                use_mlock=config.get("use_mlock", True),
                verbose=config.get("verbose", True),
                seed=config.get("seed", -1),
                offload_kqv=config.get("offload_kqv", True),
                embedding=config.get("embedding", False)
            )
            
            logger.info(f"Modelo GGUF carregado com sucesso de {model_path}")
            
            # Iniciar thread de limpeza de memória se necessário
            if should_run_gc():
                start_gc_thread()
                
            return
        except Exception as e:
            logger.error(f"Erro ao carregar modelo GGUF: {str(e)}")
            import traceback
            logger.error(f"Traceback detalhado: {traceback.format_exc()}")
            llm_gguf = None
    
    # Se não for GGUF ou se falhar, tenta carregar como GPT4All
    try:
        # Obter configurações para GPT4All
        config = get_model_config("gpt4all")
        llm = GPT4All(model=model_path, verbose=config.get("verbose", True))
        logger.info(f"Modelo GPT4All carregado do caminho: {model_path}")
        
        # Iniciar thread de limpeza de memória se necessário
        if should_run_gc():
            start_gc_thread()
    except Exception as e:
        logger.error(f"Erro ao carregar modelo GPT4All: {str(e)}")
        # Fallback: usar um LLM simulado
        llm = None

async def fetch_student_data(student_id: int) -> Dict[str, Any]:
    """
    Busca dados do aluno no backend.
    
    Args:
        student_id: O ID do aluno para buscar os dados.
        
    Returns:
        Um dicionário com os dados do aluno.
    """
    endpoint = f"{backend_url}/alunos/{student_id}/detalhes/"
    logger.info(f"Buscando dados do aluno no endpoint: {endpoint}")
    
    try:
        # Adiciona cabeçalhos para depuração
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'UniChat-LLM-Service'
        }
        
        # Busca detalhes do aluno
        response = requests.get(endpoint, headers=headers, timeout=10)
        
        logger.info(f"Resposta do backend: Status {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Dados recebidos do aluno {student_id}: {len(str(data))} bytes")
            return data
        else:
            logger.error(f"Erro ao buscar dados do aluno: Status {response.status_code}, Resposta: {response.text}")
            # Tente uma URL alternativa como fallback (acesso direto via backend)
            alt_url = f"http://backend/api/alunos/{student_id}/detalhes/"
            logger.info(f"Tentando URL alternativa: {alt_url}")
            alt_response = requests.get(alt_url, headers=headers, timeout=10)
            
            if alt_response.status_code == 200:
                data = alt_response.json()
                logger.info(f"Dados recebidos do aluno {student_id} (via URL alternativa): {len(str(data))} bytes")
                return data
            else:
                logger.error(f"Erro ao buscar dados do aluno (via URL alternativa): Status {alt_response.status_code}")
                return {}
    except Exception as e:
        logger.error(f"Exceção ao buscar dados do aluno: {str(e)}")
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
        logger.warning("Nenhum dado de aluno fornecido para criar o prompt.")
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
    
    logger.info(f"Criando prompt para aluno: {nome}, curso: {curso}, semestre: {semestre}")
    
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
    logger.info(f"Gerando resposta para pergunta: '{question}' do aluno ID: {student_id}")
    
    # Busca dados do aluno (se não fornecidos no context_data)
    student_data = context_data or await fetch_student_data(student_id)
    
    # Verifica se há dados do aluno
    if not student_data:
        logger.warning(f"Nenhum dado encontrado para o aluno ID: {student_id}, usando simulação")
    else:
        logger.info(f"Dados do aluno recuperados: {list(student_data.keys())}")
    
    # Cria um prompt de sistema
    system_prompt = create_system_prompt(student_data)
    
    # Se o modelo GGUF estiver disponível, use-o
    if llm_gguf is not None:
        try:
            # Obter configurações para a plataforma atual
            config = get_model_config("gguf")
            
            # Formato do prompt para o modelo Phi-3
            prompt = f"<|user|>\n{system_prompt.strip()}\n\nPergunta: {question}<|end|>\n<|assistant|>"
            logger.info("Gerando resposta com modelo GGUF")
            
            # Gera a resposta usando as configurações da plataforma
            output = llm_gguf(
                prompt,
                max_tokens=config.get("max_tokens", 500),
                stop=["<|end|>"],
                temperature=0.7,
                echo=False
            )
            
            # Extrai a resposta
            response = output["choices"][0]["text"].strip()
            
            logger.info(f"Resposta gerada pelo modelo GGUF: {len(response)} caracteres")
            
            # Forçar limpeza de memória em plataformas sensíveis (Mac)
            if is_mac_m1:
                gc.collect()
                
            return response
        except Exception as e:
            logger.error(f"Erro ao gerar resposta com modelo GGUF: {str(e)}")
            # Fallback para o próximo método
    
    # Se o modelo GPT4All estiver disponível, use-o
    if llm:
        try:
            # Prepara o prompt completo para GPT4All
            prompt_template = f"{system_prompt}\n\nPergunta: {question}\n\nResposta:"
            
            # Gera a resposta usando o LLM real
            logger.info("Gerando resposta com GPT4All")
            response = llm(prompt_template)
            logger.info(f"Resposta gerada pelo GPT4All: {len(response)} caracteres")
            
            # Forçar limpeza de memória em plataformas sensíveis (Mac)
            if is_mac_m1:
                gc.collect()
                
            return response.strip()
        except Exception as e:
            logger.error(f"Erro ao gerar resposta com GPT4All: {str(e)}")
            # Fallback para resposta simulada
            logger.info("Usando simulação como fallback")
            return simulate_response(question, student_data)
    
    # Usa uma resposta simulada se o LLM não estiver disponível
    logger.info("LLM não disponível, usando simulação")
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
    
    logger.info(f"Gerando resposta simulada para '{question_lower}' para o aluno {nome}")
    
    # Prefixo para respostas simuladas
    prefixo = "[SIMULAÇÃO] "
    
    # Responde com base em palavras-chave na pergunta
    if "nota" in question_lower or "avaliação" in question_lower or "prova" in question_lower:
        # Resposta sobre notas
        if student_data and "notas" in student_data and student_data["notas"]:
            disciplina = next((nota["disciplina"] for nota in student_data["notas"] if nota["disciplina"].lower() in question_lower), None)
            if disciplina:
                nota = next((nota for nota in student_data["notas"] if nota["disciplina"] == disciplina), None)
                if nota:
                    return f"{prefixo}Olá {nome}! Sua nota em {disciplina} é {nota['nota_final']}."
            
            return f"{prefixo}Olá {nome}! Você tem as seguintes notas registradas: " + ", ".join([f"{nota['disciplina']}: {nota['nota_final']}" for nota in student_data["notas"][:3]])
        return f"{prefixo}Olá {nome}! Não encontrei informações sobre suas notas no sistema. Entre em contato com a secretaria para mais detalhes."
    
    elif "horário" in question_lower or "aula" in question_lower or "disciplina" in question_lower:
        # Resposta sobre horários
        if student_data and "horarios" in student_data and student_data["horarios"]:
            disciplina = next((horario["disciplina"] for horario in student_data["horarios"] if horario["disciplina"].lower() in question_lower), None)
            if disciplina:
                horario = next((horario for horario in student_data["horarios"] if horario["disciplina"] == disciplina), None)
                if horario:
                    return f"{prefixo}Olá {nome}! Sua aula de {disciplina} é {horario['dia_semana_display']} das {horario['horario_inicio']} às {horario['horario_fim']} na sala {horario['sala']}."
            
            return f"{prefixo}Olá {nome}! Seus horários de aula são: " + "; ".join([f"{horario['disciplina']}: {horario['dia_semana_display']} {horario['horario_inicio']}-{horario['horario_fim']}" for horario in student_data["horarios"][:3]])
        return f"{prefixo}Olá {nome}! Não encontrei informações sobre seus horários no sistema. Verifique com a coordenação."
    
    elif "mensalidade" in question_lower or "financeiro" in question_lower or "pagamento" in question_lower:
        # Resposta sobre dados financeiros
        if student_data and "dados_financeiros" in student_data and student_data["dados_financeiros"]:
            dados = student_data["dados_financeiros"][0]  # Pega o primeiro registro
            return f"{prefixo}Olá {nome}! Sua próxima mensalidade no valor de R${dados['mensalidade']} vence em {dados['data_vencimento']} e está com status {dados['status_pagamento_display']}."
        return f"{prefixo}Olá {nome}! Não encontrei informações financeiras no sistema. Entre em contato com o setor financeiro."
    
    # Resposta genérica
    return f"{prefixo}Olá {nome}! Entendi sua pergunta sobre '{question}'. Como posso ajudar com mais detalhes? Você pode perguntar sobre notas, horários, mensalidades ou outros assuntos acadêmicos." 