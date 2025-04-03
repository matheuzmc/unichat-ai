# Guia de Instalação e Configuração Inicial do UniChat

Este documento contém um guia passo a passo para configurar o ambiente de desenvolvimento do projeto UniChat usando containers Docker. Seguindo estas instruções, você conseguirá criar um ambiente completo e isolado para o desenvolvimento sem instalar dependências diretamente na sua máquina.

## Pré-requisitos

Os únicos softwares que você precisa ter instalados na sua máquina são:

- Docker (20.10+) - [Instruções de instalação](https://docs.docker.com/get-docker/)
- Docker Compose (2.0+) - [Instruções de instalação](https://docs.docker.com/compose/install/)
- Git (opcional, para controle de versão)

## Etapa 1: Criar a Estrutura Básica do Projeto

1. Crie a pasta raiz do projeto:

```bash
mkdir -p unichat-ai
cd unichat-ai
```

2. Crie a estrutura de diretórios do projeto:

```bash
mkdir -p backend frontend llm docs
```

3. Verifique se a estrutura foi criada corretamente:

```bash
ls -la
```

Você deve ver os diretórios `backend`, `frontend`, `llm` e `docs`.

## Etapa 2: Configurar o Container de Banco de Dados (PostgreSQL)

1. Crie um arquivo `docker-compose.yml` na raiz do projeto:

```bash
touch docker-compose.yml
```

2. Edite o arquivo `docker-compose.yml` e adicione a configuração do PostgreSQL:

```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    container_name: unichat-db
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=unichat
      - POSTGRES_USER=unichat_user
      - POSTGRES_PASSWORD=unichat_password
    ports:
      - "5432:5432"
    restart: always
    networks:
      - unichat-network

networks:
  unichat-network:
    driver: bridge

volumes:
  postgres_data:
```

3. Inicie o container do banco de dados:

```bash
docker-compose up -d db
```

4. Verifique se o container está rodando:

```bash
docker-compose ps
```

5. Verifique os logs do banco de dados:

```bash
docker-compose logs db
```

## Etapa 3: Configurar o Container do Backend (Django)

1. Crie um arquivo `requirements.txt` no diretório `backend`:

```bash
touch backend/requirements.txt
```

2. Adicione as dependências do Django no arquivo `requirements.txt`:

```
Django>=4.2.0,<4.3.0
djangorestframework>=3.14.0,<3.15.0
psycopg2-binary>=2.9.5,<2.10.0
python-dotenv>=1.0.0,<1.1.0
gunicorn>=20.1.0,<20.2.0
```

3. Crie um `Dockerfile` para o backend:

```bash
touch backend/Dockerfile
```

4. Adicione o seguinte conteúdo ao `Dockerfile`:

```Dockerfile
FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
```

5. Atualize o `docker-compose.yml` para incluir o serviço de backend:

```yaml
version: '3.8'

services:
  db:
    # ... (configuração existente do PostgreSQL)

  backend:
    build: ./backend
    container_name: unichat-backend
    volumes:
      - ./backend:/app
    environment:
      - POSTGRES_DB=unichat
      - POSTGRES_USER=unichat_user
      - POSTGRES_PASSWORD=unichat_password
      - POSTGRES_HOST=db
      - POSTGRES_PORT=5432
      - DJANGO_SECRET_KEY=insecure-dev-key-do-not-use-in-production
      - DJANGO_DEBUG=True
      - DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
    ports:
      - "8000:8000"
    depends_on:
      - db
    restart: always
    networks:
      - unichat-network
    command: >
      sh -c "python manage.py migrate &&
             python manage.py runserver 0.0.0.0:8000"

networks:
  unichat-network:
    driver: bridge

volumes:
  postgres_data:
```

6. Crie um projeto Django dentro do container:

```bash
docker-compose run --rm backend sh -c "django-admin startproject config ."
```

7. Configure o arquivo `config/settings.py` para usar o PostgreSQL e variáveis de ambiente:

Crie um script temporário para modificar o arquivo settings.py:

```bash
touch backend/update_settings.py
```

Adicione o seguinte conteúdo ao script:

```python
import os
import re

# Caminho para o arquivo settings.py
settings_path = 'config/settings.py'

# Ler o conteúdo atual do arquivo
with open(settings_path, 'r') as file:
    content = file.read()

# Substituir a configuração de DATABASE
db_config = '''
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
'''

# Substituir a configuração de SECRET_KEY
secret_key_config = '''
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'insecure-dev-key-do-not-use-in-production')
'''

# Substituir a configuração de DEBUG
debug_config = '''
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'
'''

# Substituir a configuração de ALLOWED_HOSTS
allowed_hosts_config = '''
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
'''

# Adicionar import os no topo do arquivo se não existir
if "import os" not in content:
    content = "import os\n" + content

# Substituir configurações
content = re.sub(r"SECRET_KEY = .*", secret_key_config, content)
content = re.sub(r"DEBUG = .*", debug_config, content)
content = re.sub(r"ALLOWED_HOSTS = .*", allowed_hosts_config, content)
content = re.sub(r"DATABASES = .*?\}", db_config, content, flags=re.DOTALL)

# Escrever o conteúdo modificado de volta ao arquivo
with open(settings_path, 'w') as file:
    file.write(content)

print("Arquivo settings.py atualizado com sucesso!")
```

Execute o script para atualizar as configurações:

```bash
docker-compose run --rm backend python update_settings.py
```

8. Adicione o Django REST Framework às INSTALLED_APPS:

```bash
docker-compose run --rm backend sh -c "sed -i \"s/INSTALLED_APPS = \[/INSTALLED_APPS = \[\n    'rest_framework',/g\" config/settings.py"
```

9. Crie uma aplicação para a API:

```bash
docker-compose run --rm backend python manage.py startapp api
```

10. Inicie o container do backend:

```bash
docker-compose up -d backend
```

11. Verifique se o container está rodando:

```bash
docker-compose ps
```

12. Abra um navegador e acesse `http://localhost:8000` para verificar se o Django está funcionando corretamente. Você deve ver a página de boas-vindas do Django.

## Etapa 4: Configurar o Container do Serviço LLM

1. Crie um arquivo `requirements.txt` no diretório `llm`:

```bash
touch llm/requirements.txt
```

2. Adicione as dependências do LLM no arquivo `requirements.txt`:

```
langchain>=0.1.0,<0.2.0
fastapi>=0.104.0,<0.105.0
uvicorn>=0.23.2,<0.24.0
python-dotenv>=1.0.0,<1.1.0
pydantic>=2.4.2,<2.5.0
requests>=2.31.0,<2.32.0
```

3. Crie um `Dockerfile` para o serviço LLM:

```bash
touch llm/Dockerfile
```

4. Adicione o seguinte conteúdo ao `Dockerfile`:

```Dockerfile
FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

5. Crie a estrutura básica da aplicação LLM:

```bash
mkdir -p llm/app
touch llm/app/__init__.py
touch llm/app/main.py
```

6. Adicione um código de exemplo para o serviço LLM em `llm/app/main.py`:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI(title="UniChat LLM Service")

class QueryRequest(BaseModel):
    question: str
    student_id: int

class QueryResponse(BaseModel):
    answer: str

# Uma função de resposta simulada para o MVP
# Em uma implementação real, aqui estaria a integração com um LLM via LangChain
def generate_response(question: str, student_id: int) -> str:
    return f"Esta é uma resposta simulada para a pergunta: '{question}' do aluno {student_id}. Em uma implementação real, esta resposta seria gerada por um LLM."

@app.get("/")
def read_root():
    return {"status": "ok", "message": "UniChat LLM Service is running"}

@app.post("/api/query", response_model=QueryResponse)
def process_query(request: QueryRequest):
    try:
        answer = generate_response(request.question, request.student_id)
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

7. Atualize o `docker-compose.yml` para incluir o serviço LLM:

```yaml
version: '3.8'

services:
  db:
    # ... (configuração existente do PostgreSQL)

  backend:
    # ... (configuração existente do backend)

  llm:
    build: ./llm
    container_name: unichat-llm
    volumes:
      - ./llm:/app
    ports:
      - "8080:8080"
    environment:
      - LLM_MODEL_PATH=/app/models/model.bin
    restart: always
    networks:
      - unichat-network

networks:
  unichat-network:
    driver: bridge

volumes:
  postgres_data:
```

8. Inicie o container do serviço LLM:

```bash
docker-compose up -d llm
```

9. Verifique se o container está rodando:

```bash
docker-compose ps
```

10. Teste o serviço LLM com um comando curl (ou acessando `http://localhost:8080` no navegador):

```bash
curl http://localhost:8080
```

Você deve ver uma resposta JSON indicando que o serviço está em execução.

## Etapa 5: Configurar o Container do Frontend (React/Vite)

1. Crie um arquivo `package.json` no diretório `frontend`:

```bash
touch frontend/package.json
```

2. Adicione a configuração básica do package.json:

```json
{
  "name": "unichat-frontend",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "tailwindcss": "^3.3.3",
    "zod": "^3.22.2"
  },
  "devDependencies": {
    "@types/react": "^18.2.15",
    "@types/react-dom": "^18.2.7",
    "@vitejs/plugin-react": "^4.0.3",
    "autoprefixer": "^10.4.15",
    "postcss": "^8.4.29",
    "typescript": "^5.0.2",
    "vite": "^4.4.5"
  }
}
```

3. Crie um arquivo `Dockerfile` para o frontend:

```bash
touch frontend/Dockerfile
```

4. Adicione o seguinte conteúdo ao `Dockerfile`:

```Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
```

5. Crie um arquivo de configuração para o Vite:

```bash
touch frontend/vite.config.ts
```

6. Adicione a configuração básica do Vite:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    watch: {
      usePolling: true
    }
  }
})
```

7. Crie a estrutura básica da aplicação React:

```bash
mkdir -p frontend/src
touch frontend/src/main.tsx
touch frontend/src/App.tsx
touch frontend/index.html
```

8. Adicione o conteúdo básico ao arquivo `frontend/index.html`:

```html
<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>UniChat</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

9. Adicione o conteúdo básico ao arquivo `frontend/src/main.tsx`:

```tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

10. Adicione o conteúdo básico ao arquivo `frontend/src/App.tsx`:

```tsx
import React from 'react'

function App() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-3xl font-bold mb-4">Bem-vindo ao UniChat</h1>
      <p className="text-lg text-gray-700">
        Seu assistente acadêmico inteligente.
      </p>
    </div>
  )
}

export default App
```

11. Crie o arquivo de estilo CSS:

```bash
touch frontend/src/index.css
```

12. Adicione a configuração básica do Tailwind ao arquivo `frontend/src/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

13. Crie os arquivos de configuração do Tailwind:

```bash
touch frontend/tailwind.config.js
touch frontend/postcss.config.js
```

14. Adicione a configuração básica do Tailwind ao arquivo `frontend/tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

15. Adicione a configuração básica do PostCSS ao arquivo `frontend/postcss.config.js`:

```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

16. Atualize o `docker-compose.yml` para incluir o serviço frontend:

```yaml
version: '3.8'

services:
  db:
    # ... (configuração existente do PostgreSQL)

  backend:
    # ... (configuração existente do backend)

  llm:
    # ... (configuração existente do LLM)

  frontend:
    build: ./frontend
    container_name: unichat-frontend
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    restart: always
    networks:
      - unichat-network

networks:
  unichat-network:
    driver: bridge

volumes:
  postgres_data:
```

17. Inicie o container do frontend:

```bash
docker-compose up -d frontend
```

18. Verifique se o container está rodando:

```bash
docker-compose ps
```

19. Abra um navegador e acesse `http://localhost:3000` para verificar se o frontend está funcionando corretamente. Você deve ver uma página simples com a mensagem "Bem-vindo ao UniChat".

## Etapa 6: Verifique a Integração Completa dos Serviços

1. Verifique se todos os serviços estão funcionando corretamente:

```bash
docker-compose ps
```

Todos os serviços (db, backend, llm, frontend) devem estar no estado "Up".

2. Teste a comunicação entre os containers:

```bash
# Teste a comunicação entre o backend e o banco de dados
docker-compose exec backend python -c "import django; django.setup(); from django.db import connection; cursor = connection.cursor(); cursor.execute('SELECT 1'); print(cursor.fetchone())"

# Teste a comunicação entre o backend e o serviço LLM
docker-compose exec backend curl http://llm:8080

# Reinicie todos os serviços para garantir que tudo está funcionando corretamente
docker-compose restart
```

3. Verifique os logs de todos os serviços para identificar possíveis erros:

```bash
docker-compose logs
```

## Próximos Passos

Agora que você tem um ambiente de desenvolvimento completo configurado com Docker, você pode começar a desenvolver o projeto UniChat. Aqui estão alguns próximos passos sugeridos:

1. Implementar modelos de dados no Django conforme especificado no PRD
2. Configurar a API REST no backend
3. Implementar a integração com um LLM real no serviço LLM
4. Desenvolver a interface do chat no frontend
5. Configurar a comunicação entre o frontend e o backend

## Solução de Problemas Comuns

### Problema: Um ou mais containers não iniciam

Verifique os logs do container específico:

```bash
docker-compose logs [nome_do_serviço]
```

### Problema: Conflito de portas

Se houver algum serviço já utilizando as portas configuradas, você pode alterá-las no arquivo `docker-compose.yml`. Por exemplo, alterar `"8000:8000"` para `"8001:8000"`.

### Problema: Permissões de arquivo no volume montado

Em sistemas Linux, pode haver problemas de permissão com volumes montados. Use o seguinte comando para corrigir:

```bash
sudo chown -R $USER:$USER ./
```

### Problema: Mudanças no código não são refletidas

Reinicie o container específico:

```bash
docker-compose restart [nome_do_serviço]
```

### Problema: Pacotes não instalados no frontend

Entre no container e instale manualmente:

```bash
docker-compose exec frontend sh
npm install [nome_do_pacote]
exit
``` 