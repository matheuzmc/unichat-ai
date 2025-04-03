# API Blueprint: UniChat

Este documento descreve a estrutura inicial da API REST que será implementada para o UniChat. Trata-se de uma especificação conceitual que servirá como guia para o desenvolvimento.

## Base URL

```
/api/v1/
```

## Autenticação

Para o MVP, a autenticação será simplificada. Em versões futuras, será implementada autenticação JWT.

```
Authorization: Bearer {token}
```

## Recursos e Endpoints

### Alunos

#### Obter Dados do Aluno

```
GET /alunos/{id}/
```

**Parâmetros**
- `id` (obrigatório): ID único do aluno

**Resposta de Sucesso (200 OK)**
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao.silva@universidade.edu",
  "matricula": "202301001",
  "curso": "Engenharia de Software",
  "semestre": 3,
  "data_nascimento": "2000-05-15",
  "endereco": "Rua das Flores, 123 - São Paulo"
}
```

### Notas

#### Listar Notas do Aluno

```
GET /alunos/{id}/notas/
```

**Parâmetros**
- `id` (obrigatório): ID único do aluno
- `disciplina` (opcional): Filtrar por disciplina
- `semestre` (opcional): Filtrar por semestre

**Resposta de Sucesso (200 OK)**
```json
{
  "notas": [
    {
      "id": 101,
      "disciplina": "Matemática",
      "nota_prova": 8.5,
      "nota_trabalho": 9.0,
      "nota_final": 8.7,
      "data_avaliacao": "2023-06-10"
    },
    {
      "id": 102,
      "disciplina": "Física",
      "nota_prova": 7.0,
      "nota_trabalho": 8.5,
      "nota_final": 7.5,
      "data_avaliacao": "2023-06-15"
    }
  ]
}
```

### Horários de Aulas

#### Listar Horários do Aluno

```
GET /alunos/{id}/horarios/
```

**Parâmetros**
- `id` (obrigatório): ID único do aluno
- `dia_semana` (opcional): Filtrar por dia da semana
- `disciplina` (opcional): Filtrar por disciplina

**Resposta de Sucesso (200 OK)**
```json
{
  "horarios": [
    {
      "id": 201,
      "disciplina": "Matemática",
      "dia_semana": "Segunda-feira",
      "horario_inicio": "08:00",
      "horario_fim": "10:00",
      "sala": "Bloco A - Sala 101"
    },
    {
      "id": 202,
      "disciplina": "Física",
      "dia_semana": "Terça-feira",
      "horario_inicio": "10:00",
      "horario_fim": "12:00",
      "sala": "Bloco B - Sala 203"
    }
  ]
}
```

### Frequência

#### Listar Registros de Frequência

```
GET /alunos/{id}/frequencia/
```

**Parâmetros**
- `id` (obrigatório): ID único do aluno
- `disciplina` (opcional): Filtrar por disciplina
- `periodo_inicio` (opcional): Data de início do período
- `periodo_fim` (opcional): Data de fim do período

**Resposta de Sucesso (200 OK)**
```json
{
  "frequencia": [
    {
      "id": 301,
      "disciplina": "Matemática",
      "data": "2023-05-22",
      "status_presenca": "Presente"
    },
    {
      "id": 302,
      "disciplina": "Física",
      "data": "2023-05-23",
      "status_presenca": "Ausente"
    }
  ],
  "resumo": {
    "total_aulas": 20,
    "presencas": 18,
    "ausencias": 2,
    "percentual_presenca": 90
  }
}
```

### Dados Financeiros

#### Consultar Situação Financeira

```
GET /alunos/{id}/financeiro/
```

**Parâmetros**
- `id` (obrigatório): ID único do aluno

**Resposta de Sucesso (200 OK)**
```json
{
  "mensalidades": [
    {
      "id": 401,
      "valor": 1500.00,
      "data_vencimento": "2023-05-10",
      "status_pagamento": "Pago",
      "data_pagamento": "2023-05-08",
      "valor_pago": 1500.00
    },
    {
      "id": 402,
      "valor": 1500.00,
      "data_vencimento": "2023-06-10",
      "status_pagamento": "Pendente",
      "data_pagamento": null,
      "valor_pago": 0.00
    }
  ],
  "resumo": {
    "mensalidades_pagas": 5,
    "mensalidades_pendentes": 1,
    "valor_total_pendente": 1500.00
  }
}
```

### Matrículas

#### Consultar Matrículas do Semestre

```
GET /alunos/{id}/matriculas/
```

**Parâmetros**
- `id` (obrigatório): ID único do aluno
- `semestre` (opcional): Filtrar por semestre

**Resposta de Sucesso (200 OK)**
```json
{
  "semestre": "2023.1",
  "data_matricula": "2023-01-20",
  "disciplinas": [
    {
      "id": 501,
      "codigo": "MAT101",
      "nome": "Matemática",
      "creditos": 4,
      "professor": "Dr. Roberto Santos",
      "status": "Em andamento"
    },
    {
      "id": 502,
      "codigo": "FIS102",
      "nome": "Física",
      "creditos": 4,
      "professor": "Dra. Maria Oliveira",
      "status": "Em andamento"
    }
  ]
}
```

### Chat

#### Enviar Pergunta

```
POST /chat/perguntar/
```

**Corpo da Requisição**
```json
{
  "aluno_id": 1,
  "pergunta": "Qual foi minha nota em Matemática?"
}
```

**Resposta de Sucesso (200 OK)**
```json
{
  "id": 601,
  "pergunta": "Qual foi minha nota em Matemática?",
  "resposta": "Sua nota final na disciplina de Matemática foi 8.7, composta por 8.5 na prova e 9.0 no trabalho.",
  "timestamp": "2023-06-20T14:30:45Z",
  "dados_contextuais": {
    "tipo": "nota",
    "disciplina": "Matemática",
    "nota_final": 8.7
  }
}
```

#### Listar Histórico de Chat

```
GET /alunos/{id}/chat/historico/
```

**Parâmetros**
- `id` (obrigatório): ID único do aluno
- `limite` (opcional): Número máximo de mensagens a retornar
- `offset` (opcional): Offset para paginação

**Resposta de Sucesso (200 OK)**
```json
{
  "historico": [
    {
      "id": 601,
      "pergunta": "Qual foi minha nota em Matemática?",
      "resposta": "Sua nota final na disciplina de Matemática foi 8.7, composta por 8.5 na prova e 9.0 no trabalho.",
      "timestamp": "2023-06-20T14:30:45Z"
    },
    {
      "id": 602,
      "pergunta": "Quando é minha aula de Física?",
      "resposta": "Sua aula de Física acontece às terças-feiras, das 10:00 às 12:00, na sala 203 do Bloco B.",
      "timestamp": "2023-06-20T14:31:30Z"
    }
  ],
  "total": 2,
  "limite": 10,
  "offset": 0
}
```

## Códigos de Status

- 200 OK: Requisição bem-sucedida
- 400 Bad Request: Requisição mal formatada
- 401 Unauthorized: Autenticação necessária
- 403 Forbidden: Sem permissão para acessar o recurso
- 404 Not Found: Recurso não encontrado
- 500 Internal Server Error: Erro interno do servidor

## Paginação

Para endpoints que retornam coleções grandes de dados, a paginação será implementada usando os parâmetros `limite` e `offset`:

```
GET /alunos/{id}/notas/?limite=10&offset=0
```

A resposta incluirá metadados de paginação:

```json
{
  "notas": [...],
  "total": 25,
  "limite": 10,
  "offset": 0
}
```

## Versionamento

A API será versionada no caminho da URL. A versão inicial será a v1:

```
/api/v1/alunos/
```

## Considerações Futuras

- Implementação de autenticação JWT
- Cache de resposta para melhorar performance
- WebSockets para comunicação em tempo real
- Endpoints para feedback sobre qualidade das respostas
- API para administração e manutenção dos dados 