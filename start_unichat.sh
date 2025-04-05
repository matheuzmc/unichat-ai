#!/bin/bash

# Script para iniciar o Unichat com o LLM rodando localmente no M1
# e os outros serviços no Docker

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

# Verificar se o Docker está instalado e em execução
if ! command -v docker &> /dev/null; then
    print_error "Docker não encontrado. Por favor, instale o Docker."
    exit 1
fi

if ! docker info &> /dev/null; then
    print_error "O Docker não está em execução. Por favor, inicie o Docker Desktop."
    exit 1
fi

# Verificar se o script de configuração do LLM existe
if [ ! -f "llm/local_setup.sh" ]; then
    print_error "Script de configuração do LLM não encontrado em llm/local_setup.sh"
    exit 1
fi

# Verificar se o modelo existe
MODEL_NAME="Phi-3-mini-4k-instruct-q4.gguf"
MODEL_PATH="llm/models/$MODEL_NAME"
if [ ! -f "$MODEL_PATH" ]; then
    print_warning "Modelo não encontrado em $MODEL_PATH"
    print_msg "IMPORTANTE: O modelo deve ser baixado manualmente e colocado no diretório $MODEL_PATH antes de executar este script."
    print_msg "O processo de download do modelo NÃO é automatizado e deve ser feito previamente."
fi

# Parar containers em execução
print_msg "Parando containers em execução..."
docker-compose down

# Iniciar serviços Docker (exceto LLM)
print_msg "Iniciando serviços Docker (exceto LLM)..."
docker-compose up -d db backend frontend

# Verificar status dos containers
print_msg "Verificando status dos containers..."
sleep 5
docker ps

# Configurar e iniciar LLM local
print_msg "Configurando e iniciando o LLM local..."
cd llm
chmod +x local_setup.sh
./local_setup.sh

# Nota: o script local_setup.sh já deve perguntar ao usuário se deseja iniciar o serviço LLM
# e executá-lo se a resposta for sim 