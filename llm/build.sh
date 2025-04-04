#!/bin/bash
set -e

# Cores para saída
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Iniciando build do serviço LLM ===${NC}"

# Pergunta se deve reconstruir a imagem base
read -p "Reconstruir a imagem base? Isso é necessário apenas quando há mudanças em dependências (s/N): " rebuild_base
if [[ "$rebuild_base" =~ ^[Ss]$ ]]; then
    echo -e "${YELLOW}Construindo imagem base (isso pode demorar vários minutos)...${NC}"
    docker compose build llm-base
    echo -e "${GREEN}✓ Imagem base construída com sucesso!${NC}"
fi

# Constrói a imagem do serviço
echo -e "${YELLOW}Construindo serviço LLM...${NC}"
docker compose build llm
echo -e "${GREEN}✓ Serviço LLM construído com sucesso!${NC}"

# Pergunta se deve reiniciar o serviço
read -p "Reiniciar o serviço LLM? (s/N): " restart_service
if [[ "$restart_service" =~ ^[Ss]$ ]]; then
    echo -e "${YELLOW}Reiniciando serviço LLM...${NC}"
    docker compose up -d llm
    echo -e "${GREEN}✓ Serviço LLM reiniciado!${NC}"
fi

echo -e "${GREEN}=== Build concluído! ===${NC}" 