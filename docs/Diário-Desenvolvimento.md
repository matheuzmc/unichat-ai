# Diário de Desenvolvimento: UniChat

Este documento serve como um registro cronológico do desenvolvimento do projeto UniChat. Aqui serão documentadas decisões importantes, alterações significativas, problemas encontrados e lições aprendidas durante o processo de desenvolvimento.

## Template de Entrada

```
## [Data: AAAA-MM-DD]

### Atividades Realizadas
- Descrição da atividade 1
- Descrição da atividade 2

### Decisões Tomadas
- Decisão 1: justificativa
- Decisão 2: justificativa

### Problemas Encontrados
- Problema 1: como foi resolvido ou plano para resolução
- Problema 2: como foi resolvido ou plano para resolução

### Próximos Passos
- Tarefa planejada 1
- Tarefa planejada 2

### Observações
Quaisquer observações adicionais, insights ou ideias para o futuro.
```

## Entradas do Diário

## [Data: 2023-04-03]

### Atividades Realizadas
- Criação da documentação inicial do projeto
- Definição do PRD (Product Requirements Document)
- Elaboração do plano de implementação MVP
- Criação do glossário técnico e outros documentos de suporte

### Decisões Tomadas
- Escolha de Django REST Framework para o backend: maior produtividade e ecossistema maduro
- Escolha de React/Vite para o frontend: performance e experiência de desenvolvimento
- Decisão de usar LLM open-source: controle local e redução de custos
- Adoção do LangChain para integração de fontes de dados: simplificação da arquitetura

### Problemas Encontrados
- Indefinição sobre qual LLM open-source específico utilizar: planejado um estudo comparativo entre GPT4All e Llama2
- Preocupações sobre performance local de LLMs: necessidade de testar em ambiente representativo

### Próximos Passos
- Configurar ambiente de desenvolvimento com Docker
- Implementar estrutura básica do projeto Django
- Definir modelos de dados e criar migrações iniciais
- Inicializar projeto React/Vite com configuração de Tailwind e TypeScript

### Observações
O projeto parece promissor, mas será importante definir bem o escopo do MVP para garantir entrega dentro do prazo de 6 semanas. A integração com LLM local será o maior desafio técnico e deve ser priorizada para validação inicial.

---

<!-- Novas entradas serão adicionadas acima desta linha --> 