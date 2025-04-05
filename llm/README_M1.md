# Configuração do LLM Local para MacBook M1

Este guia explica como configurar e executar o serviço LLM localmente em um MacBook M1, enquanto os outros serviços (backend, frontend e banco de dados) continuam rodando em containers Docker.

## Contexto

O modelo de LLM (Phi-3-mini-4k-instruct) pode se beneficiar da aceleração por hardware no MacBook M1 através da API Metal da Apple. Usando essa configuração, você terá melhor desempenho comparado à execução em Docker, já que o Docker no M1 tem limitações para acesso direto à GPU.

## Requisitos

- MacBook com chip M1/M2/M3
- Python 3.10 ou superior
- Modelo Phi-3-mini-4k-instruct-q4.gguf baixado (em ~/Downloads ou no diretório do projeto)
- Docker Desktop para MacOS (para rodar os outros serviços)

## Instruções de Configuração

### 1. Configure o ambiente virtual e instale as dependências

Navegue até o diretório `llm` e execute o script de configuração:

```bash
cd llm
chmod +x local_setup.sh
./local_setup.sh
```

Este script irá:
- Verificar se o Python 3 está instalado
- Instalar o virtualenv, se necessário
- Verificar e mover o modelo LLM da pasta Downloads, se necessário
- Criar e configurar um ambiente virtual
- Instalar todas as dependências necessárias, incluindo llama-cpp-python com suporte para Metal
- Configurar o arquivo .env com os caminhos corretos

### 2. Inicie os serviços Docker (exceto o LLM)

Em outro terminal, na raiz do projeto, execute:

```bash
docker-compose up
```

O arquivo `docker-compose.override.yml` configurado excluirá automaticamente o serviço LLM do Docker, permitindo que você o execute localmente.

### 3. Inicie o serviço LLM local

No terminal onde você executou o script de configuração, execute:

```bash
# Se ainda não estiver ativado:
source venv/bin/activate

# Inicie o serviço LLM
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

## Estrutura do Projeto Modificada

- **/llm/local_setup.sh**: Script para configurar o ambiente virtual e preparar o LLM local
- **/llm/models/**: Diretório para armazenar o modelo Phi-3-mini-4k-instruct-q4.gguf
- **/llm/venv/**: Ambiente virtual Python (gerado pelo script)
- **/docker-compose.override.yml**: Configuração para desativar o LLM do Docker e conectar os serviços ao LLM local

## Verificando o Funcionamento

1. Acesse o frontend em http://localhost:3000
2. Teste o LLM enviando uma consulta
3. Verifique os logs do terminal onde o LLM está rodando

## Solução de Problemas

### O modelo não está sendo carregado corretamente

Verifique se:
- O modelo está no caminho correto (indicado nos logs)
- O ambiente virtual está ativado
- As dependências foram instaladas corretamente

### Erro de conexão entre o backend e o LLM

Verifique se:
- O serviço LLM está rodando no endereço 0.0.0.0:8080
- A configuração `host.docker.internal` está funcionando corretamente
- O firewall não está bloqueando a conexão

### Desempenho insatisfatório

- Verifique nos logs se o Metal está sendo utilizado corretamente
- Ajuste os parâmetros de configuração em `app/llm_service.py` (como número de threads)

## Comandos Úteis

- Para verificar se o Metal está sendo utilizado:
```
ps aux | grep llama
```

- Para monitorar o uso da GPU:
```
sudo powermetrics --samplers gpu_perf
```

- Para reiniciar todos os serviços:
```
docker-compose down && docker-compose up -d && cd llm && source venv/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
``` 