# Comandos de Teste para Respostas do LLM

Este diretório contém comandos personalizados do Django para testar a qualidade das respostas geradas pelo serviço LLM utilizado no projeto.

## Arquivos Disponíveis

- `test_llm_responses.py`: Comando básico para testes simples das respostas do LLM
- `test_llm_avancado.py`: Comando avançado com suporte a relatórios e testes de capacidades específicas
- `testes_prontos.py`: Biblioteca de casos de teste predefinidos usados pelo comando avançado

## Como Executar os Testes

### Teste Básico

Este comando executa testes simples verificando se as respostas do LLM contêm informações corretas para consultas básicas:

```bash
python manage.py test_llm_responses
```

Opções disponíveis:

- `--aluno_id ID`: Especifica o ID do aluno para realizar os testes
- `--disciplina NOME`: Especifica uma disciplina para focar os testes
- `--verbose`: Exibe detalhes completos de cada teste

Exemplo:

```bash
python manage.py test_llm_responses --aluno_id 42 --verbose
```

### Teste Avançado

Este comando executa testes mais completos utilizando casos predefinidos, com suporte a relatórios e análise de capacidades específicas:

```bash
python manage.py test_llm_avancado
```

Opções disponíveis:

- `--aluno_id ID`: Especifica o ID do aluno para realizar os testes
- `--categoria CATEGORIA`: Executa apenas testes de uma categoria específica (notas, horarios, info_geral, complexa, conversacao)
- `--verbose`: Exibe detalhes completos de cada teste
- `--gerar_relatorio`: Gera relatório em CSV e gráficos dos resultados
- `--testar_capacidades`: Executa testes específicos para capacidades avançadas do LLM

Exemplo:

```bash
python manage.py test_llm_avancado --categoria notas --gerar_relatorio --testar_capacidades
```

## Estrutura dos Testes

### Categorias de Teste

- **Notas**: Consultas relacionadas a notas e desempenho acadêmico
- **Horários**: Consultas sobre horários de aula, salas e cronograma
- **Informações Gerais**: Consultas sobre curso, semestre e dados do aluno
- **Complexas**: Consultas que exigem contexto adicional ou raciocínio
- **Conversação**: Testes de capacidade de manter contexto em conversas

### Capacidades Específicas do LLM

- **Formatação de Tabela**: Capacidade de apresentar dados em formato tabular
- **Atualização Recente**: Conhecimento sobre atualização de dados
- **Explicação Pedagógica**: Capacidade de fornecer explicações educativas
- **Comparação de Notas**: Habilidade de comparar categorias diferentes
- **Recomendação**: Capacidade de fazer recomendações personalizadas

## Relatórios

Quando executado com a opção `--gerar_relatorio`, o teste avançado gera:

1. Arquivo CSV com detalhes de todos os testes executados
2. Gráfico de barras mostrando a taxa de sucesso por categoria
3. Gráfico de pizza mostrando a distribuição geral dos resultados

Os relatórios são salvos no diretório `relatorios_llm/` na raiz do projeto.

## Estendendo os Testes

Para adicionar novos casos de teste, edite o arquivo `testes_prontos.py` seguindo a estrutura existente. 