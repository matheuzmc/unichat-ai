# Decisões Técnicas: UniChat

Este documento registra as decisões técnicas tomadas no projeto UniChat e suas justificativas. Servirá como referência para entender os motivos por trás das escolhas tecnológicas.

## Stack Tecnológico

### Backend

#### Django e Django REST Framework

**Decisão:** Utilizar Django 4.2+ com Django REST Framework 3.14+ para o backend.

**Justificativa:**
- Django oferece um ecossistema maduro e robusto para desenvolvimento rápido
- Django REST Framework simplifica a criação de APIs RESTful
- O ORM do Django facilita a modelagem e manipulação de dados
- Suporte nativo a migrações para controle de versão do banco de dados
- Comunidade grande e ativa, com ampla documentação
- Facilidade de integração com PostgreSQL

**Alternativas consideradas:**
- FastAPI: Mais rápido, mas com ecossistema menos maduro para o tipo de aplicação
- Flask: Mais leve, mas exigiria mais configurações manuais
- Node.js/Express: Bom para aplicações assíncronas, mas menos adequado para manipulação robusta de modelos de dados

### Banco de Dados

#### PostgreSQL

**Decisão:** Utilizar PostgreSQL 14+ como banco de dados relacional.

**Justificativa:**
- Compatibilidade excelente com Django
- Sistema de banco de dados relacional robusto e maduro
- Suporte a tipos de dados complexos e consultas avançadas
- Boa performance para o volume de dados esperado
- Transações ACID para garantir integridade dos dados
- Comunidade ativa e boa documentação

**Alternativas consideradas:**
- MySQL: Similar, mas com menos recursos avançados
- SQLite: Insuficiente para ambiente de produção
- MongoDB: Inadequado para dados altamente relacionais como os deste projeto

### Modelo de Linguagem (LLM)

#### LLM Open-Source (GPT4All/Llama2)

**Decisão:** Utilizar um LLM open-source, como GPT4All ou Llama2, para processamento de linguagem natural.

**Justificativa:**
- Modelos open-source podem ser executados localmente, sem dependência de APIs externas
- Controle total sobre o modelo e sua execução
- Sem custos recorrentes de API
- Possibilidade de fine-tuning para o domínio acadêmico
- Modelos recentes têm capacidade suficiente para as tarefas necessárias

**Alternativas consideradas:**
- OpenAI API (GPT-4): Mais potente, mas com custos de API e dependência externa
- Claude API: Excelente para seguir instruções, mas com as mesmas desvantagens da API
- Modelos menores: Insuficientes para compreensão contextual necessária

### Integração LLM

#### LangChain

**Decisão:** Utilizar LangChain para integração do LLM com fontes de dados.

**Justificativa:**
- Framework especializado para construção de aplicações com LLMs
- Facilita a conexão de LLMs com fontes de dados externas
- Suporte a ferramentas de engenharia de prompts
- Possibilidade de criar cadeias de raciocínio (chains)
- Comunidade ativa e desenvolvimento rápido
- Bom suporte a diferentes LLMs open-source

**Alternativas consideradas:**
- Implementação manual: Mais trabalhosa e propensa a erros
- LlamaIndex: Alternativa viável, mas com menos recursos para o caso de uso

### Frontend

#### React com Vite

**Decisão:** Desenvolver o frontend com React 18+ e Vite 4.0+.

**Justificativa:**
- React é uma biblioteca madura e popular para construção de interfaces
- Vite oferece builds rápidos e hot module replacement eficiente
- Excelente suporte a TypeScript
- Comunidade ativa e vasto ecossistema de bibliotecas
- Facilidade de integração com Tailwind CSS e shadcn/ui
- Possibilidade de código reutilizável e componentizado

**Alternativas consideradas:**
- Next.js: Bom para SEO e SSR, mas recursos desnecessários para aplicação de chat
- Vue.js: Bom framework, mas menor ecossistema de bibliotecas para o caso de uso
- Angular: Mais opinativo e com maior curva de aprendizado

#### TypeScript

**Decisão:** Utilizar TypeScript 5.0+ para tipagem estática.

**Justificativa:**
- Adiciona tipagem estática ao JavaScript, reduzindo erros em tempo de execução
- Melhor autocompletion e suporte IDE
- Documentação implícita através de tipos
- Refatoração mais segura
- Integração perfeita com React e Zod

**Alternativas consideradas:**
- JavaScript puro: Mais rápido para prototipar, mas menos seguro para manutenção a longo prazo
- Flow: Similar, mas com menor adoção e ecossistema

#### Tailwind CSS

**Decisão:** Utilizar Tailwind CSS 3.3+ para estilização.

**Justificativa:**
- Abordagem utility-first que acelera o desenvolvimento
- Excelente responsividade
- Fácil customização
- Boa performance em produção com purge CSS
- Integração perfeita com componentes React
- Facilidade de manutenção em equipe

**Alternativas consideradas:**
- CSS/SCSS puro: Mais trabalho manual e maior risco de duplicação de código
- Styled Components: Boa alternativa, mas com curva de aprendizado
- Material UI: Componentes prontos, mas menos flexíveis para customização

#### shadcn/ui

**Decisão:** Utilizar shadcn/ui para componentes de UI.

**Justificativa:**
- Componentes React reutilizáveis e estilizáveis
- Design moderno e acessível
- Boa integração com Tailwind CSS
- Código-fonte aberto e customizável
- Não é uma dependência, mas uma coleção de componentes

**Alternativas consideradas:**
- Chakra UI: Robusto, mas menos integrado com Tailwind
- Radix UI: Base excelente (shadcn é construído sobre Radix)
- MUI: Mais pesado e com estética Material Design

#### Zod

**Decisão:** Utilizar Zod para validação de esquemas.

**Justificativa:**
- Validação de esquemas TypeScript-first
- Excelente inferência de tipos
- Integração perfeita com React Hook Form
- API declarativa e intuitiva
- Mensagens de erro customizáveis

**Alternativas consideradas:**
- Yup: Similar, mas com definição de tipos menos robusta
- Joi: Mais antigo e menos integrado com TypeScript
- Validação manual: Trabalhosa e propensa a erros

## Infraestrutura

### Docker

**Decisão:** Utilizar Docker e Docker Compose para containerização.

**Justificativa:**
- Isolamento de serviços
- Ambiente consistente entre desenvolvimento e produção
- Facilidade de configuração de múltiplos serviços
- Simplificação do processo de deployment
- Flexibilidade para mudar componentes individuais

**Alternativas consideradas:**
- Instalação direta: Mais complexa para gerenciar dependências
- VMs: Mais pesadas e recursos intensivos
- Kubernetes: Excessivo para a escala inicial do projeto

## Persistência de Dados

**Decisão:** Armazenar histórico de conversas no banco de dados.

**Justificativa:**
- Permite análise de uso e melhoria contínua
- Possibilita recomendações baseadas no histórico
- Referência futura para perguntas similares
- Base para melhorias no modelo de linguagem

**Alternativas consideradas:**
- Sem persistência: Perda de dados valiosos para melhoria
- Armazenamento apenas em logs: Difícil consulta e análise

## Arquitetura de Software

**Decisão:** Adotar arquitetura em camadas bem definidas.

**Justificativa:**
- Separação clara de responsabilidades
- Facilidade de testes
- Componentes substituíveis individualmente
- Manutenção simplificada
- Escalabilidade modular

**Camadas:**
1. **Apresentação:** Interface de usuário React
2. **API:** Endpoints REST com Django REST Framework
3. **Serviço:** Lógica de negócio e integração com LLM
4. **Persistência:** Modelos e acesso ao banco de dados
5. **Infraestrutura:** Docker, logging, monitoramento

## Atualizações Futuras

Este documento será atualizado à medida que novas decisões técnicas forem tomadas no projeto. Cada decisão incluirá:
- Descrição clara da decisão
- Justificativa detalhada
- Alternativas consideradas
- Trade-offs aceitos 