#!/bin/bash

# Script para configurar o ambiente virtual e executar o LLM localmente no MacBook M1
# Autor: Claude - Unichat AI

# Cores para saída
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens com formatação
print_msg() {
    echo -e "${BLUE}[UniChat]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[Sucesso]${NC} $1"
}

print_error() {
    echo -e "${RED}[Erro]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[Aviso]${NC} $1"
}

# Verificar se o Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 não encontrado. Por favor, instale o Python 3."
    exit 1
fi

# Guardar o caminho do Python
PYTHON_PATH=$(which python3)
print_msg "Usando Python em: $PYTHON_PATH"

# Instalar e localizar o virtualenv
print_msg "Verificando/instalando virtualenv..."
$PYTHON_PATH -m pip install --user virtualenv

# Caminho para o virtualenv
VIRTUALENV_PATH="$($PYTHON_PATH -m pip show virtualenv | grep "Location" | cut -d' ' -f2)/virtualenv"
if [ ! -f "$VIRTUALENV_PATH/__main__.py" ]; then
    # Tentar caminho alternativo
    VIRTUALENV_PATH="$(find $HOME -name virtualenv -type d | grep site-packages | head -n 1)"
fi

print_msg "Virtualenv encontrado em: $VIRTUALENV_PATH"

# Verificar se o modelo existe na pasta de destino
MODEL_NAME="Phi-3-mini-4k-instruct-q4.gguf"
MODELS_DIR="$(pwd)/models"
LOCAL_MODEL_PATH="$MODELS_DIR/$MODEL_NAME"

mkdir -p "$MODELS_DIR"

if [ ! -f "$LOCAL_MODEL_PATH" ]; then
    print_error "Modelo não encontrado no diretório necessário: $LOCAL_MODEL_PATH"
    print_msg "Por favor, baixe o modelo manualmente e coloque-o em $MODELS_DIR com o nome $MODEL_NAME"
    print_msg "O processo de download do modelo deve ser feito manualmente e previamente à execução deste script."
    exit 1
else
    print_success "Modelo encontrado em $LOCAL_MODEL_PATH"
fi

# Configurar ambiente virtual
VENV_DIR="venv"

if [ ! -d "$VENV_DIR" ]; then
    print_msg "Criando ambiente virtual em $VENV_DIR..."
    $PYTHON_PATH -m virtualenv "$VENV_DIR"
    print_success "Ambiente virtual criado com sucesso!"
else
    print_msg "Ambiente virtual já existe em $VENV_DIR"
fi

# Ativar ambiente virtual
print_msg "Ativando ambiente virtual..."
source "$VENV_DIR/bin/activate"

# Verificar se o ambiente virtual foi ativado
if [[ "$VIRTUAL_ENV" == "" ]]; then
    print_error "Falha ao ativar o ambiente virtual. Tentando método alternativo."
    # Tentar outra forma de ativar
    ACTIVATE_SCRIPT="$VENV_DIR/bin/activate"
    if [ -f "$ACTIVATE_SCRIPT" ]; then
        source "$ACTIVATE_SCRIPT"
    else
        print_error "Arquivo de ativação não encontrado em $ACTIVATE_SCRIPT"
        exit 1
    fi
fi

# Instalar dependências para o M1
print_msg "Instalando dependências para o M1..."
pip install --upgrade pip
pip install langchain==0.1.0 fastapi==0.100.0 uvicorn==0.22.0 python-dotenv==1.0.0 pydantic==2.0.3 
pip install requests==2.31.0 langchain-community==0.0.11 chromadb==0.4.15

# Instalando llama-cpp-python com suporte para GPU Metal
print_msg "Instalando llama-cpp-python com suporte para Metal no M1..."
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python

print_success "Dependências instaladas com sucesso!"

# Criar arquivo .env
ENV_FILE=".env"
print_msg "Criando arquivo de ambiente $ENV_FILE..."

cat > "$ENV_FILE" << EOL
LLM_MODEL_PATH=$(pwd)/models/Phi-3-mini-4k-instruct-q4.gguf
BACKEND_URL=http://localhost:8000/api
EOL

print_success "Arquivo de ambiente criado com sucesso!"

# Instruções para executar
print_success "Configuração concluída!"

# Verificar se está em um Mac com processador ARM
is_mac_arm=false
if [[ "$(uname)" == "Darwin" && "$(uname -m)" == "arm64" ]]; then
    is_mac_arm=true
    print_msg "Detectado MacBook com chip M1/M2/M3 (ARM)"
fi

# Iniciar o serviço automaticamente em Macs com ARM
if $is_mac_arm; then
    print_msg "Iniciando o serviço LLM automaticamente..."
    if command -v uvicorn &> /dev/null; then
        uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
    else
        print_error "Comando uvicorn não encontrado. Tentando com caminho explícito."
        $VENV_DIR/bin/uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
    fi
else
    # Para outros sistemas, mostra as instruções e pergunta
    print_msg "Para iniciar o serviço LLM, execute:"
    print_msg "  source $VENV_DIR/bin/activate"
    print_msg "  uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload"

    # Perguntar se o usuário deseja iniciar o serviço agora
    read -p "Deseja iniciar o serviço LLM agora? (s/n): " INICIAR

    if [[ "$INICIAR" =~ ^[Ss]$ ]]; then
        print_msg "Iniciando o serviço LLM..."
        if command -v uvicorn &> /dev/null; then
            uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
        else
            print_error "Comando uvicorn não encontrado. Tentando com caminho explícito."
            $VENV_DIR/bin/uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
        fi
    else
        print_msg "O serviço não será iniciado agora. Use os comandos acima quando estiver pronto."
    fi
fi 