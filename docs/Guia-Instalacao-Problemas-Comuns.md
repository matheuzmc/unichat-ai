# Guia de Problemas Comuns e Soluções: UniChat

Este documento compila os problemas mais comuns encontrados durante a instalação e configuração do projeto UniChat, juntamente com suas soluções. Utilize-o como referência quando encontrar dificuldades semelhantes.

## Problemas de Permissão

### Problema: Permissões de Arquivos em Volumes Docker

**Sintoma:** 
Arquivos criados dentro dos containers pertencem ao usuário root, impedindo edição no host sem sudo.

**Solução 1: Configuração de UID/GID**
1. Crie um arquivo `.env` na raiz do projeto:
   ```bash
   echo "UID=$(id -u)" > .env
   echo "GID=$(id -g)" >> .env
   ```

2. Configure o `docker-compose.yml` para usar essas variáveis:
   ```yaml
   services:
     backend:
       user: "${UID}:${GID}"
       # outras configurações...
   ```

**Solução 2: Ajuste de Permissões Existentes**
```bash
sudo chown -R $USER:$USER ./
```

### Problema: O PostgreSQL Falha com Configuração user: "${UID}:${GID}"

**Sintoma:**
Erro semelhante a: `chmod: changing permissions of '/var/lib/postgresql/data': Operation not permitted`

**Solução:**
Remova a configuração `user: "${UID}:${GID}"` apenas do serviço `db` no `docker-compose.yml`. O PostgreSQL precisa ser executado como o usuário `postgres` dentro do container.

### Problema: Frontend com Erros de Permissão em node_modules

**Sintoma:**
Erros como `EACCES: permission denied, mkdir '/app/node_modules/.vite'`

**Solução:**
Configure um volume anônimo para o diretório node_modules:
```yaml
frontend:
  # ...
  volumes:
    - ./frontend:/app
    - /app/node_modules  # Volume anônimo para node_modules
```

## Problemas de Conexão

### Problema: Backend Não Consegue Conectar ao Banco de Dados

**Sintoma:**
Erro como: `could not translate host name "db" to address: Temporary failure in name resolution`

**Solução:**
Adicione um healthcheck para o PostgreSQL e configure o backend para depender dele:

```yaml
db:
  # ...
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U unichat_user -d unichat"]
    interval: 5s
    timeout: 5s
    retries: 5

backend:
  # ...
  depends_on:
    db:
      condition: service_healthy
```

### Problema: Pacote Curl Não Disponível no Container Backend

**Sintoma:**
Erro ao executar `curl` dentro do container: `curl: command not found`

**Solução:**
Adicione o pacote curl ao Dockerfile do backend:
```Dockerfile
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

## Problemas de Configuração Django

### Problema: Erro na Configuração de DATABASES no settings.py

**Sintoma:**
Erro de sintaxe: `SyntaxError: unmatched '}'`

**Solução:**
Edite manualmente o arquivo `backend/config/settings.py` e verifique se a estrutura do dicionário DATABASES está correta:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'unichat'),
        'USER': os.environ.get('POSTGRES_USER', 'unichat_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'unichat_password'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}
```

### Problema: Módulo settings Não Encontrado em Comandos Python

**Sintoma:**
Erro como: `ModuleNotFoundError: No module named 'config'` ao executar comandos Python no container

**Solução:**
Defina explicitamente a variável de ambiente DJANGO_SETTINGS_MODULE:

```bash
docker compose exec backend python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings'); import django; django.setup(); [resto do comando]"
```

## Problemas com Docker Compose

### Problema: Versão do Docker Compose Obsoleta

**Sintoma:**
Aviso sobre a versão (`version: '3.8'`) ser obsoleta

**Solução:**
Remova a linha `version: '3.8'` do arquivo `docker-compose.yml`. As versões recentes do Docker Compose não exigem mais essa especificação.

### Problema: Erros de Indentação no docker-compose.yml

**Sintoma:**
Erros indicando que um serviço está definido dentro de outro

**Solução:**
Verifique e corrija a indentação no arquivo `docker-compose.yml`. Todos os serviços devem estar no mesmo nível de indentação abaixo de `services:`.

## Dicas Gerais

### Verificar Logs dos Containers

```bash
docker compose logs [nome_do_serviço]
```

### Reiniciar um Serviço Específico

```bash
docker compose restart [nome_do_serviço]
```

### Entrar no Shell de um Container

```bash
docker compose exec [nome_do_serviço] bash
# ou
docker compose exec [nome_do_serviço] sh
```

### Limpar Tudo e Recomeçar

```bash
docker compose down -v
docker compose up -d
```

O argumento `-v` remove os volumes, útil quando você quer um estado completamente novo. 

## Problemas com o Serviço LLM

### Problema: Instalação da Biblioteca llama-cpp-python

**Sintoma:**
Erro ao instalar ou importar a biblioteca llama-cpp-python, necessária para modelos GGUF.

**Solução 1: Instalação em Diretório Personalizado**
```bash
docker exec -it unichat-llm bash -c "mkdir -p /tmp/llama_cpp_install && export CMAKE_ARGS='-DGGML_CUDA=OFF' && pip install llama-cpp-python==0.2.79 --no-cache-dir --force-reinstall --target=/tmp/llama_cpp_install"
```

Depois, adicione este diretório ao Python PATH no início do arquivo `llm/app/llm_service.py`:
```python
import sys
sys.path.insert(0, '/tmp/llama_cpp_install')
```

**Solução 2: Instalação com Dependências Específicas**
Se a solução 1 não funcionar, tente adicionar as dependências necessárias no Dockerfile do LLM:
```Dockerfile
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    git \
    cmake \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

### Problema: Erro na Importação de Módulos

**Sintoma:**
Erro como: `NameError: name 'llama_cpp' is not defined`

**Solução:**
Use a importação correta no arquivo `llm/app/llm_service.py`:
```python
try:
    import llama_cpp
    has_llama_cpp = True
    logger.info("llama-cpp-python importado com sucesso!")
except ImportError:
    logger.warning("llama-cpp-python não está disponível. O modelo GGUF não será utilizado.")
    has_llama_cpp = False
```

E quando for instanciar o modelo, use:
```python
llm_gguf = llama_cpp.Llama(
    model_path=model_path,
    n_ctx=4096,
    n_threads=4
)
```

### Problema: Modelo GGUF Não Está Sendo Utilizado

**Sintoma:**
O sistema continua usando o modo de simulação mesmo com o modelo GGUF disponível.

**Solução:**
Verifique a configuração do `LLM_MODEL_PATH` no arquivo `docker-compose.yml`:
```yaml
environment:
  - LLM_MODEL_PATH=/app/models/Phi-3-mini-4k-instruct-q4.gguf
```

E verifique se as verificações de tipo de arquivo estão corretas no código:
```python
is_gguf = model_path.endswith('.gguf')
if is_gguf and has_llama_cpp:
    # Carregar modelo GGUF
```

### Problema: Erro ao Carregar Modelo GGUF

**Sintoma:**
Erro como: `libllama.so: cannot open shared object file: No such file or directory`

**Solução:**
Este erro geralmente indica problemas com as dependências nativas. Tente reconstruir a imagem LLM com as configurações corretas:

```bash
docker compose build --no-cache llm
docker compose up -d llm
```

### Problema: Versão Incompatível de llama-cpp-python

**Sintoma:**
Erros de incompatibilidade de versão ou métodos não encontrados.

**Solução:**
Use uma versão específica que sabemos funcionar:
```bash
docker exec -it unichat-llm pip install llama-cpp-python==0.2.79 --no-cache-dir --force-reinstall
```

### Problema: Erro de Permissão ao Acessar Modelo GGUF

**Sintoma:**
Erro de permissão ao tentar ler o arquivo do modelo.

**Solução:**
Ajuste as permissões do arquivo de modelo:
```bash
sudo chmod 644 llm/models/Phi-3-mini-4k-instruct-q4.gguf
```

Ou reconstrua o contêiner com a configuração correta de usuário:
```yaml
services:
  llm:
    user: "${UID}:${GID}"
```

## Instalação do Modelo GGUF (Passo a Passo)

1. **Baixe o modelo GGUF**
   ```bash
   # Crie o diretório para modelos
   mkdir -p llm/models
   
   # Baixe o modelo (exemplo com wget)
   wget -O llm/models/Phi-3-mini-4k-instruct-q4.gguf https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-GGUF/blob/main/Phi-3-mini-4k-instruct-q4.gguf
   
   # Alternativa: baixe manualmente e coloque no diretório llm/models
   ```

2. **Atualize o docker-compose.yml**
   ```yaml
   services:
     llm:
       environment:
         - LLM_MODEL_PATH=/app/models/Phi-3-mini-4k-instruct-q4.gguf
   ```

3. **Modifique o código do LLM para usar o modelo GGUF**
   Certifique-se de que o arquivo `llm/app/llm_service.py` tenha:
   ```python
   import sys
   sys.path.insert(0, '/tmp/llama_cpp_install')
   
   try:
       import llama_cpp
       has_llama_cpp = True
   except ImportError:
       has_llama_cpp = False
   ```

4. **Instale a biblioteca llama-cpp-python**
   ```bash
   docker exec -it unichat-llm bash -c "mkdir -p /tmp/llama_cpp_install && export CMAKE_ARGS='-DGGML_CUDA=OFF' && pip install llama-cpp-python==0.2.79 --no-cache-dir --force-reinstall --target=/tmp/llama_cpp_install"
   ```

5. **Reinicie o serviço LLM**
   ```bash
   docker compose restart llm
   ```

6. **Verifique nos logs se o modelo foi carregado corretamente**
   ```bash
   docker compose logs llm | grep "Modelo GGUF carregado com sucesso"
   ``` 