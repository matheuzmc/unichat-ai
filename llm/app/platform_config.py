"""
Configurações específicas por plataforma para o LLM.
Este arquivo centraliza as configurações que devem variar por plataforma.
"""
import platform
import os
import logging

logger = logging.getLogger(__name__)

# Detectar plataforma
is_macos = platform.system() == "Darwin"
is_arm = platform.machine() == "arm64"
is_mac_m1 = is_macos and is_arm
is_linux = platform.system() == "Linux"

logger.info(f"Plataforma detectada: {platform.system()} {platform.machine()}")
logger.info(f"Mac com Apple Silicon: {is_mac_m1}")

# Definir o limite de memória por plataforma
if is_mac_m1:
    # Configuração otimizada para Mac com chip Apple Silicon
    LLM_CONFIG = {
        # Configurações gerais
        "gc_interval": 60,      # Intervalo para coleta de lixo (segundos)
        
        # Configurações GGUF (llama.cpp)
        "gguf": {
            "n_ctx": 2048,        # Tamanho do contexto reduzido (era 4096)
            "n_batch": 128,       # Tamanho do lote reduzido (era 512)
            "n_threads": 4,       # Menos threads
            "n_gpu_layers": 20,   # Menos camadas na GPU (era 40)
            "use_mlock": False,   # Não bloquear na RAM
            "verbose": False,     # Reduzir logs
            "offload_kqv": True,  # Manter offload para GPU
            "seed": -1,
            "embedding": False,   # Desativar embeddings
            "max_tokens": 300,    # Limitar tokens de saída
        },
        
        # Configurações para outros tipos de LLM
        "gpt4all": {
            "verbose": False,
            "n_threads": 4,
        }
    }
else:
    # Configuração padrão para outras plataformas (Linux, etc.)
    LLM_CONFIG = {
        # Configurações gerais
        "gc_interval": 120,     # Intervalo para coleta de lixo (segundos)
        
        # Configurações GGUF (llama.cpp)
        "gguf": {
            "n_ctx": 4096,        # Tamanho do contexto original
            "n_batch": 512,       # Tamanho do lote original
            "n_threads": 6,       # Threads originais
            "n_gpu_layers": 40,   # Camadas na GPU originais
            "use_mlock": True,    # Bloquear na RAM
            "verbose": True,      # Logs completos
            "offload_kqv": True,  # Offload para GPU
            "seed": -1,
            "embedding": False,   # Desativar embeddings
            "max_tokens": 500,    # Tokens de saída originais
        },
        
        # Configurações para outros tipos de LLM
        "gpt4all": {
            "verbose": True,
            "n_threads": 6,
        }
    }

def get_model_config(model_type="gguf"):
    """Retorna a configuração apropriada para o tipo de modelo."""
    if model_type in LLM_CONFIG:
        return LLM_CONFIG[model_type]
    return {}

def should_run_gc():
    """Indica se a coleta de lixo periódica deve ser executada nesta plataforma."""
    # No Mac, sempre executamos a coleta de lixo periódica
    return is_mac_m1 