# Glossário Técnico: UniChat

Este documento contém definições dos principais termos técnicos utilizados no projeto UniChat para facilitar a compreensão rápida dos conceitos por todas as partes envolvidas.

## Termos Gerais

- **MVP (Produto Mínimo Viável)**: Versão do produto com funcionalidades mínimas necessárias para validar o conceito com usuários reais.

- **LLM (Large Language Model)**: Modelo de linguagem de grande escala treinado em grandes quantidades de texto, capaz de entender e gerar linguagem natural.

- **MCP (Model Context Protocol)**: Protocolo customizado para gerenciar o contexto do modelo de linguagem, permitindo consultas eficientes a dados externos.

- **NLP (Natural Language Processing)**: Processamento de Linguagem Natural, campo da IA focado em interações entre computadores e linguagem humana.

## Termos de Arquitetura

- **API REST**: Interface de Programação de Aplicações que segue os princípios REST (Representational State Transfer) para comunicação entre sistemas.

- **Endpoint**: Ponto de acesso específico em uma API REST que representa uma funcionalidade ou recurso.

- **Serializer**: Componente que converte dados complexos (como objetos Django) em formatos facilmente consumíveis (como JSON).

- **Prompt**: Instrução ou pergunta fornecida a um LLM para guiar a geração de resposta.

## Tecnologias

- **Django**: Framework web Python de alto nível que incentiva o desenvolvimento rápido e design limpo.

- **Django REST Framework (DRF)**: Extensão do Django para construir APIs RESTful.

- **React**: Biblioteca JavaScript para construir interfaces de usuário.

- **Vite**: Ferramenta de build moderna para desenvolvimento frontend.

- **TypeScript**: Superset tipado do JavaScript que melhora a segurança do código.

- **Tailwind CSS**: Framework CSS utility-first para desenvolvimento rápido.

- **shadcn/ui**: Biblioteca de componentes UI para React.

- **Zod**: Biblioteca TypeScript para validação de esquemas.

- **LangChain**: Framework para desenvolvimento de aplicações potencializadas por LLMs.

- **Docker**: Plataforma para desenvolvimento, envio e execução de aplicações em containers.

- **PostgreSQL**: Sistema de gerenciamento de banco de dados relacional.

## Componentes do Sistema UniChat

- **Frontend Chat**: Interface de usuário onde os alunos interagem com o sistema através de perguntas em linguagem natural.

- **Backend API**: Serviço Django que expõe endpoints RESTful para acesso aos dados acadêmicos e administrativos.

- **Serviço LLM**: Componente responsável por processar perguntas, entender a intenção e gerar respostas em linguagem natural.

- **Banco de Dados**: Armazenamento de informações acadêmicas e administrativas dos alunos.

## Conceitos de Dados

- **Modelo de Dados**: Estrutura que define como os dados são organizados, armazenados e manipulados.

- **Entidade**: Objeto ou conceito do mundo real representado no banco de dados (ex: Aluno, Nota).

- **Relacionamento**: Conexão entre diferentes entidades no banco de dados.

- **Migração**: Processo de versionamento e alteração da estrutura do banco de dados de forma controlada.

## Métricas e Avaliação

- **Tempo de Resposta**: Tempo entre o envio da pergunta e o recebimento da resposta.

- **Taxa de Acerto**: Porcentagem de perguntas para as quais o sistema fornece uma resposta correta e relevante.

- **Uptime**: Tempo em que o sistema está disponível e funcionando corretamente.

- **Satisfação do Usuário**: Medida qualitativa da experiência do usuário com o sistema. 