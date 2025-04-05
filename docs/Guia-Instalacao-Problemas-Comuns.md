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

## Problemas ao Baixar o Modelo GGUF

## Otimizações de Performance para o Modelo GGUF

Esta seção descreve como implementar as otimizações que melhoram significativamente o tempo de resposta do modelo GGUF no serviço LLM.

### Implementando o Sistema de Cache

Para implementar o sistema de cache em dois níveis que reduz drasticamente o tempo de respostas repetidas:

1. Edite o arquivo `llm_service.py`:

```python
# No topo do arquivo, adicione:
import time
from datetime import datetime

# Defina os dicionários de cache
_student_data_cache = {}
_response_cache = {}

# Modifique a função fetch_student_data para usar cache
async def fetch_student_data(student_id):
    cache_key = student_id
    
    # Verificar se os dados já estão em cache
    if cache_key in _student_data_cache:
        print(f"Usando dados em cache para aluno ID: {student_id}")
        return _student_data_cache[cache_key]
    
    # Se não estiverem em cache, buscar do backend
    try:
        print(f"Buscando dados do aluno ID: {student_id}")
        # Seu código existente para buscar dados...
        
        # Armazenar no cache antes de retornar
        _student_data_cache[cache_key] = student_data
        return student_data
    except Exception as e:
        print(f"Erro ao buscar dados do aluno: {e}")
        raise

# Modifique a função handle_query para usar cache de resposta
async def handle_query(question, student_id):
    # Criar uma chave única para esta combinação de pergunta e aluno
    cache_key = f"{student_id}:{question}"
    
    # Verificar se a resposta já está em cache
    if cache_key in _response_cache:
        print(f"Usando resposta em cache para pergunta: '{question}'")
        return _response_cache[cache_key]
    
    # Se não estiver em cache, gerar a resposta
    start_time = time.time()
    print(f"Gerando resposta para: '{question}'")
    
    # Seu código existente para gerar a resposta...
    
    # Armazenar no cache antes de retornar
    elapsed_time = time.time() - start_time
    print(f"Resposta gerada em {elapsed_time:.2f} segundos")
    _response_cache[cache_key] = response
    return response
```

### Otimizando os Parâmetros do Modelo

Para otimizar os parâmetros do modelo GGUF:

1. Edite o arquivo `llm_service.py` para ajustar os parâmetros do modelo:

```python
# Na inicialização do modelo, ajuste:
llm = LlamaCpp(
    model_path="/app/models/Phi-3-mini-4k-instruct-q4.gguf",
    temperature=0.1,           # Reduzido de 0.7
    max_tokens=150,            # Reduzido de 500
    n_ctx=1024,                # Reduzido de 4096
    n_batch=1024,              # Aumentado de 512
    n_threads=12,              # Aumentado de 4
    verbose=False,             # Desativar logs verbosos
    # Configurações adicionais
    top_p=0.95,
    f16_kv=True,               # Usar half precision para KV cache
    streaming=False,
    seed=-1                    # Use uma seed fixa para resultados mais consistentes
)
```

### Implementando o Pré-aquecimento do Modelo

Para pré-aquecer o modelo e melhorar o tempo de resposta inicial:

```python
# No arquivo llm_service.py, antes do app.get("/")
async def warm_up_model():
    """Pré-aquece o modelo executando uma inferência simples."""
    try:
        print("Pré-aquecendo o modelo...")
        start_time = time.time()
        
        # Inferência simples para aquecer o modelo
        prompt = "Responda 'OK' para confirmar que o modelo está funcionando."
        await llm.ainvoke(prompt)
        
        elapsed_time = time.time() - start_time
        print(f"Modelo pré-aquecido em {elapsed_time:.2f} segundos")
    except Exception as e:
        print(f"Erro ao pré-aquecer o modelo: {e}")

# Modificar a inicialização da aplicação
@app.on_event("startup")
async def startup_event():
    """Executa tarefas de inicialização."""
    await warm_up_model()
```

### Otimizando o Sistema de Prompts

Para reduzir o tamanho dos prompts e melhorar o tempo de resposta:

```python
# No arquivo llm_service.py, otimize o template do prompt
def create_prompt(question, student_data):
    """Cria um prompt otimizado para o modelo LLM."""
    # Versão otimizada com menos tokens
    template = """
    Você é um assistente universitário chamado UniChat. Responda à seguinte pergunta 
    usando apenas os dados fornecidos. Seja breve e direto.
    
    DADOS DO ALUNO:
    {student_data}
    
    PERGUNTA: {question}
    
    RESPOSTA:
    """
    
    # Formatar os dados do aluno de forma compacta
    formatted_data = []
    for key, value in student_data.items():
        if isinstance(value, list):
            formatted_data.append(f"{key}: {', '.join(str(item) for item in value)}")
        else:
            formatted_data.append(f"{key}: {value}")
    
    student_data_str = "\n".join(formatted_data)
    
    # Criar o prompt completo
    prompt = template.format(student_data=student_data_str, question=question)
    return prompt
```

### Estratégia de Build em Duas Camadas

Para reduzir drasticamente o tempo de build durante o desenvolvimento:

1. Modifique o `Dockerfile.llm` para usar uma abordagem em duas camadas:

```dockerfile
# Primeira camada: compilação do llama-cpp-python
FROM python:3.10-slim AS builder

# Instalar dependências de compilação
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Compilar llama-cpp-python otimizado para CPU
RUN pip install --no-cache-dir llama-cpp-python==0.2.11+cpuavx2 setuptools wheel

# Segunda camada: imagem de runtime
FROM python:3.10-slim

# Copiar os pacotes instalados da camada builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Instalar dependências de runtime
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /app

# Copiar apenas os arquivos necessários
COPY requirements-llm.txt /app/
RUN pip install --no-cache-dir -r requirements-llm.txt

# Copiar código da aplicação
COPY llm_service.py /app/

# Diretório para o modelo
RUN mkdir -p /app/models
VOLUME /app/models

# Expor porta
EXPOSE 8080

# Iniciar a aplicação FastAPI
CMD ["uvicorn", "llm_service:app", "--host", "0.0.0.0", "--port", "8080"]
```

2. Atualize o arquivo `docker-compose.yml` para usar o novo Dockerfile:

```yaml
  llm:
    build:
      context: .
      dockerfile: Dockerfile.llm
    restart: always
    volumes:
      - ./Phi-3-mini-4k-instruct-q4.gguf:/app/models/Phi-3-mini-4k-instruct-q4.gguf
    ports:
      - "8080:8080"
```

### Verificação de Performance

Após implementar estas otimizações, verifique se você está obtendo os tempos de resposta esperados:

1. **Primeira consulta**: Em torno de 2-3 minutos
2. **Segunda consulta (modelo aquecido)**: Em torno de 20-30 segundos
3. **Consulta em cache**: Menos de 100ms

Se os tempos forem significativamente maiores, verifique os seguintes pontos:

1. Confirme se o sistema de cache está funcionando (verifique os logs)
2. Verifique se os parâmetros do modelo foram corretamente ajustados
3. Verifique se o hardware tem recursos suficientes (especialmente CPU) 

## Problemas Específicos do MacOS com Apple Silicon (M1/M2/M3)

### Problema: Serviço LLM não Inicia Automaticamente no M1/M2/M3

**Sintoma:**
Após executar `./start_unichat.sh`, o LLM não é iniciado automaticamente ou não é detectado pelo sistema.

**Solução:**
Verifique se o script `local_setup.sh` detecta corretamente a arquitetura ARM:

```bash
# Verificar a saída de:
uname -a
```

Se a saída contiver "arm64", mas o LLM não foi iniciado automaticamente, verifique a função de detecção no script:

```bash
# Edite o arquivo llm/local_setup.sh e verifique se possui:
if [[ "$(uname)" == "Darwin" && "$(uname -m)" == "arm64" ]]; then
    is_mac_arm=true
fi
```

### Problema: LLM Local não Utiliza Aceleração Metal no M1/M2/M3

**Sintoma:**
O LLM está rodando, mas com desempenho abaixo do esperado ou mensagens de erro sobre Metal no log.

**Solução:**
Certifique-se de que o llama-cpp-python foi instalado com suporte a Metal:

```bash
cd llm
source venv/bin/activate
pip uninstall -y llama-cpp-python
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python
```

Depois, verifique se o código está configurado para utilizar o Metal:

```python
# Em llm/app/llm_service.py deve haver:
if is_mac_m1:
    llm_gguf = llama_cpp.Llama(
        model_path=model_path,
        n_ctx=4096,
        n_gpu_layers=40,
        use_mlock=True,
        offload_kqv=True
    )
```

### Problema: Modelo LLM não Encontrado no MacOS

**Sintoma:**
Erro indicando que o modelo não foi encontrado em `llm/models/Phi-3-mini-4k-instruct-q4.gguf`.

**Solução:**
1. Verifique se o arquivo existe:
```bash
ls -la llm/models/
```

2. Se o arquivo não existir, baixe-o manualmente e coloque-o no diretório correto:
```bash
mkdir -p llm/models
# Baixe o modelo de uma fonte confiável e coloque-o em llm/models/
```

3. Verifique as permissões do arquivo:
```bash
chmod 644 llm/models/Phi-3-mini-4k-instruct-q4.gguf
```

### Problema: Banco de Dados não é Populado Automaticamente no MacOS

**Sintoma:**
Ao iniciar o sistema no MacOS, o banco de dados está vazio, sem dados de exemplo.

**Solução:**
Verifique se o arquivo `docker-compose.override.yml` contém o comando para popular o banco:

```yaml
backend:
  command: >
    sh -c "python manage.py migrate &&
           python manage.py populate_db &&
           python manage.py runserver 0.0.0.0:8000"
```

Se não, edite o arquivo ou execute manualmente:

```bash
docker exec -it unichat-backend python manage.py populate_db
```

### Problema: Erro de Memória ao Carregar o LLM no MacOS

**Sintoma:**
O serviço LLM encerra com erro relacionado à falta de memória (OOM) ao tentar carregar o modelo.

**Solução:**
1. Ajuste os parâmetros do modelo para usar menos memória:

```python
# Em llm/app/llm_service.py, ajuste:
llm_gguf = llama_cpp.Llama(
    model_path=model_path,
    n_ctx=1024,  # Reduzir o contexto
    n_gpu_layers=20,  # Reduzir camadas na GPU
    use_mlock=True
)
```

2. Feche aplicativos que consomem muita memória
3. Considere usar um modelo mais leve 