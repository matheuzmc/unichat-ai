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