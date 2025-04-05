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

## Decisões de Implementação do Backend [Atualização: 2023-04-03]

### Modelos de Dados

**Decisão:** Criar modelos detalhados para representar as entidades acadêmicas.

**Justificativa:**
- Estrutura de dados completa para atender todos os casos de uso
- Relacionamentos bem definidos utilizando chaves estrangeiras
- Campos tipados adequadamente para cada tipo de dado
- Validadores para garantir a integridade dos dados (ex: notas entre 0 e 10)
- Campos de metadados para rastreamento (created_at, updated_at)

**Modelos implementados:**
- Aluno: Informações pessoais e acadêmicas dos estudantes
- Nota: Histórico de avaliações por disciplina
- HorarioAula: Agenda de aulas por semana
- Frequencia: Registro de presença nas aulas
- DadoFinanceiro: Situação financeira e pagamentos
- Matricula: Registro de matrícula por semestre
- DisciplinaMatriculada: Disciplinas cursadas por matrícula
- ChatHistorico: Registro de interações com o sistema

### API REST

**Decisão:** Adotar REST como padrão de API com Django REST Framework ViewSets.

**Justificativa:**
- ViewSets simplificam a criação de endpoints CRUD
- Facilidade de implementação de filtros e ordenação
- Serialização padronizada dos modelos para JSON
- Integração com navegação de API para testes manuais
- Documentação automática com Swagger

**Padrões adotados:**
- ModelViewSet para operações CRUD completas
- Actions personalizadas para endpoints específicos (ex: `/alunos/{id}/detalhes/`)
- Endpoints de filtro por relacionamento (ex: `/notas/por_aluno/?aluno_id=1`)
- Serializers aninhados para relacionamentos (ex: disciplinas em matrículas)
- Campos extras em serializers para melhor contexto (ex: aluno_nome)

### Documentação da API

**Decisão:** Utilizar drf-yasg para documentação interativa da API.

**Justificativa:**
- Geração automática de documentação a partir do código
- Interface Swagger para teste interativo dos endpoints
- Alternativa ReDoc para documentação mais limpa
- Facilita o entendimento e uso da API pelos desenvolvedores frontend
- Possibilidade de customização da documentação

### Populamento do Banco de Dados

**Decisão:** Criar comandos personalizados para reset e populamento do banco de dados.

**Justificativa:**
- Dados fictícios realistas para desenvolvimento e testes
- Comando único para limpar e repopular o banco
- Relacionamentos corretamente estabelecidos entre entidades
- Facilita testes de integração e UI
- Possibilidade de ajuste dos parâmetros de geração de dados

### Internacionalização

**Decisão:** Configurar o Django para suporte ao Português do Brasil.

**Justificativa:**
- Adequação ao público-alvo brasileiro
- Mensagens de erro e validação em português
- Formatação de datas e números no padrão brasileiro
- Possibilidade de extensão para outros idiomas no futuro

### Segurança

**Decisão:** Implementar autenticação básica inicialmente, com planos para JWT.

**Justificativa:**
- Autenticação básica simples para fase inicial de desenvolvimento
- Todos os endpoints exigem autenticação (exceto documentação)
- Plano de migração para JWT para aplicações móveis/SPA
- Proteção contra acesso não autorizado aos dados

## Atualizações Futuras

Este documento será atualizado à medida que novas decisões técnicas forem tomadas no projeto. Cada decisão incluirá:
- Descrição clara da decisão
- Justificativa detalhada
- Alternativas consideradas
- Trade-offs aceitos

## Decisões de Otimização para Mac [Atualização: 2024-04-07]

### Otimização do LLM para Mac com Apple Silicon

**Decisão:** Implementar configurações e otimizações específicas para Macs com chips M1/M2/M3.

**Justificativa:**
- Aproveitar o hardware específico do Mac com Apple Silicon (API Metal)
- Melhora significativa de performance para usuários de MacBooks
- Redução do consumo de memória e prevenção de vazamentos
- Experiência de usuário mais fluida em hardware Apple

**Implementações específicas:**
- Criação de arquivo `platform_config.py` para gerenciar configurações por plataforma
- Detecção automática de sistema operacional e arquitetura
- Thread dedicado de limpeza de memória para Macs
- Monitoramento periódico do uso de memória via psutil
- Ajuste de parâmetros do modelo (n_ctx, n_batch, n_threads) para otimização em Apple Silicon
- Configuração de n_gpu_layers para aproveitar a GPU integrada via Metal

**Alternativas consideradas:**
- Emulação x86 via Rosetta 2: descartada por performance inferior
- Configuração única para todas as plataformas: descartada por subutilizar o hardware Apple
- Bibliotecas de otimização de terceiros: descartadas por questões de manutenibilidade

## Decisões de Interface do Usuário [Atualização: 2024-04-07]

### Indicador de Digitação (Typing Indicator)

**Decisão:** Implementar um indicador visual de "digitação" durante o processamento das consultas pelo LLM.

**Justificativa:**
- Feedback visual ao usuário durante o processamento das consultas
- Redução da percepção de tempo de espera
- Padrão de UX comum em interfaces de chat modernas
- Melhor experiência de usuário sem alterações de backend

**Implementação:**
- Criação de componente React dedicado (`TypingIndicator.tsx`)
- Integração com o componente ChatWindow para exibição durante estados de loading
- Animação customizada de "bolhas digitando" para feedback visual
- Utilização do componente Skeleton do shadcn/ui para versão alternativa

**Alternativas consideradas:**
- Spinner de carregamento genérico: muito impessoal para interface de chat
- Barra de progresso: inadequada para processamento de linguagem natural
- Mensagem estática de "processando": menos engajadora que a animação

### Componentes de UI Reutilizáveis

**Decisão:** Adotar e integrar a biblioteca shadcn/ui para componentes React reutilizáveis.

**Justificativa:**
- Componentes React reutilizáveis e estilizáveis
- Integração perfeita com Tailwind CSS
- Código-fonte aberto e customizável
- Base de design consistente para a aplicação
- Não é uma dependência tradicional, mas uma coleção de componentes

**Implementações específicas:**
- Integração do componente Skeleton para indicadores de carregamento
- Estilização consistente com o tema da aplicação
- Reutilização de componentes para reduzir duplicação de código

**Alternativas consideradas:**
- Uso de componentes personalizados: mais trabalho de manutenção
- Material UI: estética não alinhada com a visão do projeto
- Chakra UI: menos integrado com Tailwind CSS 