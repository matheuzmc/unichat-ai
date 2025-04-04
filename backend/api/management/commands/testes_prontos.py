"""
Este arquivo contém exemplos de consultas e respostas esperadas para testes automatizados.
É usado pelo comando test_llm_responses.py para testes mais avançados.
"""

TESTES_CONSULTAS = [
    # Consultas sobre notas
    {
        "categoria": "notas",
        "pergunta": "Qual é a minha nota em Cálculo I?",
        "termos_esperados": ["nota", "Cálculo I", "aprovado", "reprovado"],
        "contexto_necessario": False
    },
    {
        "categoria": "notas",
        "pergunta": "Quais são minhas menores notas este semestre?",
        "termos_esperados": ["nota", "baixa", "menor"],
        "contexto_necessario": False
    },
    {
        "categoria": "notas",
        "pergunta": "Eu passei em todas as disciplinas?",
        "termos_esperados": ["aprovado", "reprovado", "disciplina"],
        "contexto_necessario": False
    },
    
    # Consultas sobre horários
    {
        "categoria": "horarios",
        "pergunta": "Qual é o meu horário na segunda-feira?",
        "termos_esperados": ["segunda", "hora", "sala", "disciplina"],
        "contexto_necessario": False
    },
    {
        "categoria": "horarios",
        "pergunta": "Em qual sala tenho aula de Física?",
        "termos_esperados": ["sala", "Física", "horário"],
        "contexto_necessario": False
    },
    {
        "categoria": "horarios",
        "pergunta": "Quantas aulas tenho por semana?",
        "termos_esperados": ["aulas", "semana", "total"],
        "contexto_necessario": False
    },
    
    # Consultas sobre informações gerais
    {
        "categoria": "info_geral",
        "pergunta": "Qual curso estou fazendo?",
        "termos_esperados": ["curso", "faculdade"],
        "contexto_necessario": False
    },
    {
        "categoria": "info_geral",
        "pergunta": "Qual é o meu RA?",
        "termos_esperados": ["RA", "registro", "acadêmico", "número"],
        "contexto_necessario": False
    },
    {
        "categoria": "info_geral",
        "pergunta": "Em qual ano/semestre estou?",
        "termos_esperados": ["ano", "semestre"],
        "contexto_necessario": False
    },
    
    # Consultas complexas que exigem contexto
    {
        "categoria": "complexa",
        "pergunta": "Que disciplinas tenho amanhã?",
        "termos_esperados": ["amanhã", "disciplina", "aula"],
        "contexto_necessario": True,
        "contexto": "data_atual" # Requer saber a data atual para determinar "amanhã"
    },
    {
        "categoria": "complexa",
        "pergunta": "Quanto preciso tirar na próxima prova para passar?",
        "termos_esperados": ["prova", "nota", "passar", "média", "precisa"],
        "contexto_necessario": True,
        "contexto": "disciplina_atual" # Requer saber a qual disciplina se refere
    },
    {
        "categoria": "complexa",
        "pergunta": "Como está meu desempenho este semestre?",
        "termos_esperados": ["desempenho", "média", "notas", "semestre"],
        "contexto_necessario": True,
        "contexto": "semestre_atual" # Requer saber qual é o semestre atual
    },
    
    # Consultas com conversação
    {
        "categoria": "conversacao",
        "pergunta_inicial": "Quais são minhas disciplinas este semestre?",
        "pergunta_sequencia": "E quais são os professores?",
        "termos_esperados": ["professor", "disciplina", "leciona"],
        "contexto_necessario": True
    },
    {
        "categoria": "conversacao",
        "pergunta_inicial": "Quando é a próxima prova de Cálculo?",
        "pergunta_sequencia": "E qual é o conteúdo?",
        "termos_esperados": ["conteúdo", "prova", "Cálculo", "matéria"],
        "contexto_necessario": True
    },
    {
        "categoria": "conversacao",
        "pergunta_inicial": "Qual é minha média em Física?",
        "pergunta_sequencia": "Qual foi minha última nota?",
        "termos_esperados": ["última", "nota", "Física", "prova"],
        "contexto_necessario": True
    }
]

# Exemplos de consultas com capacidades específicas a testar
CAPACIDADES_LLMS = [
    {
        "capacidade": "formatacao_tabela",
        "pergunta": "Mostre todas as minhas disciplinas e notas em formato de tabela",
        "verificacao": lambda resposta: "|" in resposta and "-" in resposta,
        "descricao": "Capacidade de formatar dados em tabelas"
    },
    {
        "capacidade": "atualizacao_recente",
        "pergunta": "Quando foi a última vez que minhas notas foram atualizadas?",
        "verificacao": lambda resposta: "data" in resposta.lower() or "atualiza" in resposta.lower(),
        "descricao": "Conhecimento sobre atualizações de dados"
    },
    {
        "capacidade": "explicacao_pedagogica",
        "pergunta": "Explique o sistema de cálculo de médias da universidade",
        "verificacao": lambda resposta: len(resposta.split()) > 30,
        "descricao": "Capacidade de explicar sistemas educacionais"
    },
    {
        "capacidade": "comparacao_notas",
        "pergunta": "Compare meu desempenho nas disciplinas de exatas e humanas",
        "verificacao": lambda resposta: "exatas" in resposta.lower() and "humanas" in resposta.lower(),
        "descricao": "Capacidade de fazer comparações entre diferentes categorias"
    },
    {
        "capacidade": "recomendacao",
        "pergunta": "Com base nas minhas notas, qual disciplina eu deveria me dedicar mais?",
        "verificacao": lambda resposta: "dedicar" in resposta.lower() or "focar" in resposta.lower() or "atenção" in resposta.lower(),
        "descricao": "Capacidade de fazer recomendações personalizadas"
    }
] 