# API Blueprint: UniChat

Este documento descreve a estrutura da API REST implementada para o UniChat. Este blueprint reflete a implementação atual (2023-04-03) e serve como referência para desenvolvedores.

## Base URL

```
/api/
```

## Autenticação

A API utiliza autenticação básica do Django REST Framework. Para acessar recursos protegidos, utilize:

```
Authorization: Basic {base64(username:password)}
```

## Documentação Interativa

A API possui documentação interativa disponível através do Swagger UI e ReDoc:

- **Swagger UI**: `/swagger/`
- **ReDoc**: `/redoc/`

## Recursos e Endpoints

### Alunos

#### Listar/Criar Alunos

```
GET /api/alunos/
POST /api/alunos/
```

**Filtros disponíveis**
- `curso`: Filtrar por curso
- `semestre`: Filtrar por semestre
- `search`: Busca por nome, matrícula ou email

**Resposta de Sucesso (200 OK)**
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/alunos/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "nome": "Aluno Teste 1",
      "email": "aluno1@example.com",
      "matricula": "20230001",
      "curso": "Ciência da Computação",
      "semestre": 3,
      "data_nascimento": "2000-05-15",
      "endereco": "Rua Exemplo, 123, Bairro Teste, Cidade Exemplo",
      "created_at": "2023-04-05T15:30:45Z",
      "updated_at": "2023-04-05T15:30:45Z"
    },
    // ...mais alunos
  ]
}
```

#### Recuperar/Atualizar/Excluir Aluno

```
GET /api/alunos/{id}/
PUT /api/alunos/{id}/
PATCH /api/alunos/{id}/
DELETE /api/alunos/{id}/
```

**Parâmetros**
- `id` (obrigatório): ID único do aluno

**Resposta de Sucesso (200 OK)**
```json
{
  "id": 1,
  "nome": "Aluno Teste 1",
  "email": "aluno1@example.com",
  "matricula": "20230001",
  "curso": "Ciência da Computação",
  "semestre": 3,
  "data_nascimento": "2000-05-15",
  "endereco": "Rua Exemplo, 123, Bairro Teste, Cidade Exemplo",
  "created_at": "2023-04-05T15:30:45Z",
  "updated_at": "2023-04-05T15:30:45Z"
}
```

#### Obter Detalhes Completos do Aluno

```
GET /api/alunos/{id}/detalhes/
```

**Parâmetros**
- `id` (obrigatório): ID único do aluno

**Resposta de Sucesso (200 OK)**
```json
{
  "id": 1,
  "nome": "Aluno Teste 1",
  "email": "aluno1@example.com",
  "matricula": "20230001",
  "curso": "Ciência da Computação",
  "semestre": 3,
  "data_nascimento": "2000-05-15",
  "endereco": "Rua Exemplo, 123, Bairro Teste, Cidade Exemplo",
  "created_at": "2023-04-05T15:30:45Z",
  "updated_at": "2023-04-05T15:30:45Z",
  "notas": [
    // lista de notas
  ],
  "horarios": [
    // lista de horários
  ],
  "frequencias": [
    // lista de frequências
  ],
  "dados_financeiros": [
    // lista de dados financeiros
  ],
  "matriculas": [
    // lista de matrículas
  ],
  "historico_chat": [
    // histórico de chat
  ]
}
```

### Notas

#### Listar/Criar Notas

```
GET /api/notas/
POST /api/notas/
```

**Filtros disponíveis**
- `aluno`: ID do aluno
- `disciplina`: Filtrar por disciplina
- `semestre`: Filtrar por semestre

**Resposta de Sucesso (200 OK)**
```json
{
  "count": 448,
  "next": "http://localhost:8000/api/notas/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "aluno": 1,
      "aluno_nome": "Aluno Teste 1",
      "disciplina": "Programação I",
      "nota_prova": "8.50",
      "nota_trabalho": "9.00",
      "nota_final": "8.65",
      "data_avaliacao": "2023-03-10",
      "semestre": "2023.1",
      "created_at": "2023-04-05T15:30:45Z",
      "updated_at": "2023-04-05T15:30:45Z"
    },
    // ...mais notas
  ]
}
```

#### Filtrar Notas por Aluno

```
GET /api/notas/por_aluno/?aluno_id={id}
```

**Parâmetros**
- `aluno_id` (obrigatório): ID único do aluno

### Horários de Aulas

#### Listar/Criar Horários

```
GET /api/horarios/
POST /api/horarios/
```

**Filtros disponíveis**
- `aluno`: ID do aluno
- `dia_semana`: Filtrar por dia da semana (SEG, TER, QUA, QUI, SEX, SAB, DOM)
- `semestre`: Filtrar por semestre

**Resposta de Sucesso (200 OK)**
```json
{
  "count": 224,
  "next": "http://localhost:8000/api/horarios/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "aluno": 1,
      "aluno_nome": "Aluno Teste 1",
      "disciplina": "Algoritmos e Estruturas de Dados",
      "dia_semana": "SEG",
      "dia_semana_display": "Segunda-feira",
      "horario_inicio": "08:00:00",
      "horario_fim": "10:00:00",
      "sala": "A101",
      "professor": "Dr. Silva",
      "semestre": "2023.1",
      "created_at": "2023-04-05T15:30:45Z",
      "updated_at": "2023-04-05T15:30:45Z"
    },
    // ...mais horários
  ]
}
```

#### Filtrar Horários por Aluno

```
GET /api/horarios/por_aluno/?aluno_id={id}
```

**Parâmetros**
- `aluno_id` (obrigatório): ID único do aluno

### Frequência

#### Listar/Criar Frequências

```
GET /api/frequencias/
POST /api/frequencias/
```

**Filtros disponíveis**
- `aluno`: ID do aluno
- `disciplina`: Filtrar por disciplina
- `status`: Filtrar por status (PRESENTE, AUSENTE, JUSTIFICADO)
- `data`: Filtrar por data

**Resposta de Sucesso (200 OK)**
```json
{
  "count": 3360,
  "next": "http://localhost:8000/api/frequencias/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "aluno": 1,
      "aluno_nome": "Aluno Teste 1",
      "disciplina": "Algoritmos e Estruturas de Dados",
      "data": "2023-03-20",
      "status": "PRESENTE",
      "status_display": "Presente",
      "created_at": "2023-04-05T15:30:45Z",
      "updated_at": "2023-04-05T15:30:45Z"
    },
    // ...mais frequências
  ]
}
```

#### Filtrar Frequências por Aluno

```
GET /api/frequencias/por_aluno/?aluno_id={id}
```

**Parâmetros**
- `aluno_id` (obrigatório): ID único do aluno

### Dados Financeiros

#### Listar/Criar Dados Financeiros

```
GET /api/financeiro/
POST /api/financeiro/
```

**Filtros disponíveis**
- `aluno`: ID do aluno
- `status_pagamento`: Filtrar por status (PAGO, PENDENTE, ATRASADO, ISENTO)

**Resposta de Sucesso (200 OK)**
```json
{
  "count": 300,
  "next": "http://localhost:8000/api/financeiro/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "aluno": 1,
      "aluno_nome": "Aluno Teste 1",
      "mensalidade": "950.00",
      "data_vencimento": "2023-04-10",
      "status_pagamento": "PENDENTE",
      "status_pagamento_display": "Pendente",
      "data_pagamento": null,
      "valor_pago": null,
      "descricao": "Mensalidade 4/2023",
      "created_at": "2023-04-05T15:30:45Z",
      "updated_at": "2023-04-05T15:30:45Z"
    },
    // ...mais dados financeiros
  ]
}
```

#### Filtrar Dados Financeiros por Aluno

```
GET /api/financeiro/por_aluno/?aluno_id={id}
```

**Parâmetros**
- `aluno_id` (obrigatório): ID único do aluno

### Matrículas

#### Listar/Criar Matrículas

```
GET /api/matriculas/
POST /api/matriculas/
```

**Filtros disponíveis**
- `aluno`: ID do aluno
- `semestre`: Filtrar por semestre

**Resposta de Sucesso (200 OK)**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/matriculas/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "aluno": 1,
      "aluno_nome": "Aluno Teste 1",
      "semestre": "2023.1",
      "data_matricula": "2023-01-15",
      "disciplinas": [
        // lista de disciplinas matriculadas
      ],
      "created_at": "2023-04-05T15:30:45Z",
      "updated_at": "2023-04-05T15:30:45Z"
    },
    // ...mais matrículas
  ]
}
```

#### Filtrar Matrículas por Aluno

```
GET /api/matriculas/por_aluno/?aluno_id={id}
```

**Parâmetros**
- `aluno_id` (obrigatório): ID único do aluno

### Disciplinas Matriculadas

#### Listar/Criar Disciplinas Matriculadas

```
GET /api/disciplinas-matriculadas/
POST /api/disciplinas-matriculadas/
```

**Filtros disponíveis**
- `matricula`: ID da matrícula
- `status`: Filtrar por status (EM_ANDAMENTO, APROVADO, REPROVADO, TRANCADO)

**Resposta de Sucesso (200 OK)**
```json
{
  "count": 518,
  "next": "http://localhost:8000/api/disciplinas-matriculadas/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "matricula": 1,
      "codigo": "CC001",
      "nome": "Algoritmos e Estruturas de Dados I",
      "creditos": 4,
      "professor": "Dr. Silva",
      "status": "EM_ANDAMENTO",
      "status_display": "Em andamento",
      "created_at": "2023-04-05T15:30:45Z",
      "updated_at": "2023-04-05T15:30:45Z"
    },
    // ...mais disciplinas
  ]
}
```

#### Filtrar Disciplinas por Matrícula

```
GET /api/disciplinas-matriculadas/por_matricula/?matricula_id={id}
```

**Parâmetros**
- `matricula_id` (obrigatório): ID único da matrícula

### Histórico de Chat

#### Listar/Criar Histórico de Chat

```
GET /api/chat-historico/
POST /api/chat-historico/
```

**Filtros disponíveis**
- `aluno`: ID do aluno

**Resposta de Sucesso (200 OK)**
```json
{
  "count": 306,
  "next": "http://localhost:8000/api/chat-historico/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "aluno": 1,
      "aluno_nome": "Aluno Teste 1",
      "pergunta": "Qual é o horário da disciplina de Banco de Dados?",
      "resposta": "Suas aulas de Banco de Dados são às terças-feiras, das 19:00 às 21:00, na sala B201.",
      "timestamp": "2023-04-05T14:30:45Z",
      "dados_contextuais": {
        "intenção": "consulta_horario",
        "confiança": 0.95,
        "entidades_identificadas": 2
      }
    },
    // ...mais históricos
  ]
}
```

#### Filtrar Histórico por Aluno

```
GET /api/chat-historico/por_aluno/?aluno_id={id}
```

**Parâmetros**
- `aluno_id` (obrigatório): ID único do aluno

## Paginação

A API utiliza paginação por padrão com 10 itens por página. Você pode controlar a paginação com os seguintes parâmetros:

```
GET /api/alunos/?page=2
```

A resposta inclui metadados de paginação:

```json
{
  "count": 50,        // Total de itens
  "next": "http://localhost:8000/api/alunos/?page=3",   // URL da próxima página
  "previous": "http://localhost:8000/api/alunos/?page=1", // URL da página anterior
  "results": [...]   // Itens da página atual
}
```

## Filtragem, Busca e Ordenação

A API suporta:

1. **Filtragem**: Use parâmetros de consulta para filtrar resultados
   ```
   GET /api/alunos/?curso=Ciência da Computação
   ```

2. **Busca**: Use o parâmetro `search` para buscar em campos específicos
   ```
   GET /api/alunos/?search=Silva
   ```

3. **Ordenação**: Use o parâmetro `ordering` para ordenar resultados
   ```
   GET /api/notas/?ordering=-nota_final  // Ordem decrescente
   GET /api/alunos/?ordering=nome        // Ordem crescente
   ```

## Códigos de Status

- 200 OK: Requisição bem-sucedida
- 201 Created: Recurso criado com sucesso
- 204 No Content: Recurso excluído com sucesso
- 400 Bad Request: Requisição mal formatada
- 401 Unauthorized: Autenticação necessária
- 403 Forbidden: Sem permissão para acessar o recurso
- 404 Not Found: Recurso não encontrado
- 500 Internal Server Error: Erro interno do servidor

## Próximos Passos

- Implementação de autenticação JWT
- Endpoints para integração com LLM
- API de feedback sobre respostas do chat
- Cache para melhorar performance
- WebSockets para comunicação em tempo real 