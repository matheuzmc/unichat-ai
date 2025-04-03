import random
from datetime import datetime, timedelta, date
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import (
    Aluno, Nota, HorarioAula, Frequencia, DadoFinanceiro, 
    Matricula, DisciplinaMatriculada, ChatHistorico
)

class Command(BaseCommand):
    help = 'Popula o banco de dados com informações fictícias para teste'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando população do banco de dados...'))
        
        self.criar_alunos()
        self.criar_notas()
        self.criar_horarios()
        self.criar_frequencias()
        self.criar_dados_financeiros()
        self.criar_matriculas()
        self.criar_historico_chat()
        
        self.stdout.write(self.style.SUCCESS('População do banco de dados concluída com sucesso!'))
    
    def criar_alunos(self):
        self.stdout.write('Criando alunos...')
        
        cursos = [
            'Ciência da Computação', 'Engenharia de Software', 
            'Sistemas de Informação', 'Análise e Desenvolvimento de Sistemas',
            'Engenharia Civil', 'Medicina', 'Direito', 'Administração'
        ]
        
        # Criar 50 alunos fictícios
        for i in range(1, 51):
            nome = f"Aluno Teste {i}"
            matricula = f"2023{i:04d}"
            email = f"aluno{i}@example.com"
            curso = random.choice(cursos)
            semestre = random.randint(1, 10)
            
            # Data de nascimento entre 18 e 30 anos atrás
            anos_atras = random.randint(18, 30)
            data_nascimento = date.today() - timedelta(days=anos_atras*365)
            
            endereco = f"Rua Exemplo, {random.randint(1, 999)}, Bairro Teste, Cidade Exemplo"
            
            Aluno.objects.create(
                nome=nome,
                email=email,
                matricula=matricula,
                curso=curso,
                semestre=semestre,
                data_nascimento=data_nascimento,
                endereco=endereco
            )
        
        self.stdout.write(self.style.SUCCESS(f'Criados {Aluno.objects.count()} alunos'))
    
    def criar_notas(self):
        self.stdout.write('Criando notas...')
        
        disciplinas = [
            'Programação I', 'Algoritmos e Estruturas de Dados', 
            'Banco de Dados', 'Engenharia de Software', 
            'Redes de Computadores', 'Sistemas Operacionais',
            'Inteligência Artificial', 'Cálculo I',
            'Estatística', 'Física'
        ]
        
        alunos = Aluno.objects.all()
        
        # Para cada aluno, criar notas em algumas disciplinas
        for aluno in alunos:
            # Escolher aleatoriamente entre 3 e 6 disciplinas
            disciplinas_aluno = random.sample(disciplinas, random.randint(3, 6))
            
            for disciplina in disciplinas_aluno:
                # Criar notas para o semestre atual e anterior
                for semestre_str in [f"2023.{random.randint(1, 2)}", f"2022.{random.randint(1, 2)}"]:
                    # Notas aleatórias entre 0 e 10 com duas casas decimais
                    nota_prova = Decimal(str(round(random.uniform(4, 10), 2)))
                    nota_trabalho = Decimal(str(round(random.uniform(5, 10), 2)))
                    
                    # Usar Decimal em vez de float para os pesos
                    peso_prova = Decimal('0.7')
                    peso_trabalho = Decimal('0.3')
                    nota_final = (nota_prova * peso_prova + nota_trabalho * peso_trabalho).quantize(Decimal('0.01'))
                    
                    # Data aleatória nos últimos 6 meses
                    dias_atras = random.randint(1, 180)
                    data_avaliacao = date.today() - timedelta(days=dias_atras)
                    
                    Nota.objects.create(
                        aluno=aluno,
                        disciplina=disciplina,
                        nota_prova=nota_prova,
                        nota_trabalho=nota_trabalho,
                        nota_final=nota_final,
                        data_avaliacao=data_avaliacao,
                        semestre=semestre_str
                    )
        
        self.stdout.write(self.style.SUCCESS(f'Criadas {Nota.objects.count()} notas'))
    
    def criar_horarios(self):
        self.stdout.write('Criando horários de aula...')
        
        disciplinas = [
            'Programação I', 'Algoritmos e Estruturas de Dados', 
            'Banco de Dados', 'Engenharia de Software', 
            'Redes de Computadores', 'Sistemas Operacionais',
            'Inteligência Artificial', 'Cálculo I',
            'Estatística', 'Física'
        ]
        
        professores = [
            'Dr. Silva', 'Dra. Oliveira', 'Prof. Santos', 
            'Prof. Costa', 'Dra. Lima', 'Dr. Almeida',
            'Profa. Pereira', 'Dr. Fernandes'
        ]
        
        salas = ['A101', 'A102', 'B201', 'B202', 'C301', 'C302', 'D401', 'D402']
        dias_semana = ['SEG', 'TER', 'QUA', 'QUI', 'SEX']
        
        alunos = Aluno.objects.all()
        
        # Para cada aluno, criar horários para algumas disciplinas
        for aluno in alunos:
            # Escolher aleatoriamente entre 3 e 6 disciplinas
            disciplinas_aluno = random.sample(disciplinas, random.randint(3, 6))
            
            # Criar horários para cada disciplina
            for i, disciplina in enumerate(disciplinas_aluno):
                # Escolher um dia da semana aleatório
                dia_semana = dias_semana[i % len(dias_semana)]
                
                # Horário de início aleatório entre 8h e 18h
                hora_inicio = random.randint(8, 18)
                minuto_inicio = random.choice([0, 30])
                horario_inicio = f"{hora_inicio:02d}:{minuto_inicio:02d}"
                
                # Aula de 1h30min ou 2h
                duracao = random.choice([90, 120])
                
                # Calcular horário de término
                hora_fim = hora_inicio
                minuto_fim = minuto_inicio + duracao
                
                if minuto_fim >= 60:
                    hora_fim += minuto_fim // 60
                    minuto_fim = minuto_fim % 60
                
                horario_fim = f"{hora_fim:02d}:{minuto_fim:02d}"
                
                HorarioAula.objects.create(
                    aluno=aluno,
                    disciplina=disciplina,
                    dia_semana=dia_semana,
                    horario_inicio=horario_inicio,
                    horario_fim=horario_fim,
                    sala=random.choice(salas),
                    professor=random.choice(professores),
                    semestre='2023.1'
                )
        
        self.stdout.write(self.style.SUCCESS(f'Criados {HorarioAula.objects.count()} horários de aula'))
    
    def criar_frequencias(self):
        self.stdout.write('Criando frequências...')
        
        status_opcoes = ['PRESENTE', 'AUSENTE', 'JUSTIFICADO']
        
        # Usar os horários existentes para criar frequências
        horarios = HorarioAula.objects.all()
        
        for horario in horarios:
            # Criar frequências para os últimos 15 dias de aula
            for i in range(1, 16):
                # Calcular a data da aula (considerando apenas os dias da semana corretos)
                data_base = date.today() - timedelta(days=i*7)
                
                # Distribuição de frequência (70% presente, 20% ausente, 10% justificado)
                probabilidades = [0.7, 0.2, 0.1]
                status = random.choices(status_opcoes, weights=probabilidades)[0]
                
                Frequencia.objects.create(
                    aluno=horario.aluno,
                    disciplina=horario.disciplina,
                    data=data_base,
                    status=status
                )
        
        self.stdout.write(self.style.SUCCESS(f'Criadas {Frequencia.objects.count()} frequências'))
    
    def criar_dados_financeiros(self):
        self.stdout.write('Criando dados financeiros...')
        
        status_opcoes = ['PAGO', 'PENDENTE', 'ATRASADO', 'ISENTO']
        
        alunos = Aluno.objects.all()
        
        # Para cada aluno, criar dados financeiros para os últimos 6 meses
        for aluno in alunos:
            # Mensalidade base entre R$ 800 e R$ 2000
            mensalidade_base = Decimal(str(round(random.uniform(800, 2000), 2)))
            
            for i in range(6):
                # Mês atual e os 5 anteriores
                data_vencimento = date.today().replace(day=10) - timedelta(days=i*30)
                
                # Status baseado na data
                if i == 0:  # Mês atual
                    status = random.choices(['PENDENTE', 'PAGO'], weights=[0.7, 0.3])[0]
                elif i >= 1 and i <= 2:  # 1-2 meses atrás
                    status = random.choices(['PAGO', 'ATRASADO'], weights=[0.9, 0.1])[0]
                else:  # 3+ meses atrás
                    status = 'PAGO'
                
                # Data de pagamento (se foi pago)
                data_pagamento = None
                if status == 'PAGO':
                    # Pagamento entre 1 e 5 dias antes do vencimento
                    dias_antes = random.randint(1, 5)
                    data_pagamento = data_vencimento - timedelta(days=dias_antes)
                
                # Valor pago (se foi pago)
                valor_pago = None
                if status == 'PAGO':
                    # 10% de chance de desconto
                    if random.random() < 0.1:
                        valor_pago = mensalidade_base * Decimal('0.95')  # 5% de desconto
                    else:
                        valor_pago = mensalidade_base
                
                DadoFinanceiro.objects.create(
                    aluno=aluno,
                    mensalidade=mensalidade_base,
                    data_vencimento=data_vencimento,
                    status_pagamento=status,
                    data_pagamento=data_pagamento,
                    valor_pago=valor_pago,
                    descricao=f"Mensalidade {data_vencimento.month}/{data_vencimento.year}"
                )
        
        self.stdout.write(self.style.SUCCESS(f'Criados {DadoFinanceiro.objects.count()} dados financeiros'))
    
    def criar_matriculas(self):
        self.stdout.write('Criando matrículas e disciplinas matriculadas...')
        
        status_opcoes = ['EM_ANDAMENTO', 'APROVADO', 'REPROVADO', 'TRANCADO']
        
        # Lista de disciplinas por curso
        disciplinas_por_curso = {
            'Ciência da Computação': [
                ('CC001', 'Algoritmos e Estruturas de Dados I', 4),
                ('CC002', 'Programação Orientada a Objetos', 4),
                ('CC003', 'Banco de Dados', 4),
                ('CC004', 'Sistemas Operacionais', 4),
                ('CC005', 'Redes de Computadores', 4),
                ('CC006', 'Inteligência Artificial', 4),
                ('CC007', 'Compiladores', 4),
                ('MAT001', 'Cálculo I', 4),
                ('MAT002', 'Cálculo II', 4),
                ('MAT003', 'Álgebra Linear', 4),
            ],
            'Engenharia de Software': [
                ('ES001', 'Engenharia de Requisitos', 4),
                ('ES002', 'Gerência de Projetos', 4),
                ('ES003', 'Teste de Software', 4),
                ('ES004', 'Arquitetura de Software', 4),
                ('ES005', 'Desenvolvimento Ágil', 4),
                ('CC001', 'Algoritmos e Estruturas de Dados I', 4),
                ('CC002', 'Programação Orientada a Objetos', 4),
                ('CC003', 'Banco de Dados', 4),
                ('MAT001', 'Cálculo I', 4),
            ],
            'Sistemas de Informação': [
                ('SI001', 'Sistemas de Informação', 4),
                ('SI002', 'Gestão de TI', 4),
                ('SI003', 'Governança de TI', 4),
                ('SI004', 'Business Intelligence', 4),
                ('SI005', 'Gestão do Conhecimento', 4),
                ('CC001', 'Algoritmos e Estruturas de Dados I', 4),
                ('CC002', 'Programação Orientada a Objetos', 4),
                ('CC003', 'Banco de Dados', 4),
                ('MAT001', 'Cálculo I', 4),
            ],
        }
        
        # Professores por disciplina
        professores = {
            'Algoritmos e Estruturas de Dados I': 'Dr. Silva',
            'Programação Orientada a Objetos': 'Dra. Oliveira',
            'Banco de Dados': 'Prof. Santos',
            'Sistemas Operacionais': 'Prof. Costa',
            'Redes de Computadores': 'Dra. Lima',
            'Inteligência Artificial': 'Dr. Almeida',
            'Compiladores': 'Profa. Pereira',
            'Cálculo I': 'Dr. Fernandes',
            'Cálculo II': 'Dra. Souza',
            'Álgebra Linear': 'Prof. Martins',
            'Engenharia de Requisitos': 'Dr. Oliveira',
            'Gerência de Projetos': 'Profa. Costa',
            'Teste de Software': 'Dr. Pereira',
            'Arquitetura de Software': 'Dra. Almeida',
            'Desenvolvimento Ágil': 'Prof. Fernandes',
            'Sistemas de Informação': 'Dra. Lima',
            'Gestão de TI': 'Prof. Santos',
            'Governança de TI': 'Dra. Oliveira',
            'Business Intelligence': 'Dr. Silva',
            'Gestão do Conhecimento': 'Profa. Pereira',
        }
        
        alunos = Aluno.objects.all()
        
        # Para cada aluno, criar matrícula para o semestre atual
        for aluno in alunos:
            semestre_atual = '2023.1'
            
            # Criar matrícula
            matricula = Matricula.objects.create(
                aluno=aluno,
                semestre=semestre_atual,
                data_matricula=date.today() - timedelta(days=random.randint(30, 90))
            )
            
            # Obter disciplinas disponíveis para o curso do aluno
            disciplinas_curso = disciplinas_por_curso.get(
                aluno.curso, disciplinas_por_curso['Ciência da Computação']
            )
            
            # Escolher aleatoriamente entre 4 e 6 disciplinas
            num_disciplinas = random.randint(4, 6)
            disciplinas_aluno = random.sample(disciplinas_curso, min(num_disciplinas, len(disciplinas_curso)))
            
            # Criar disciplinas matriculadas
            for codigo, nome, creditos in disciplinas_aluno:
                status = 'EM_ANDAMENTO'  # Para o semestre atual, todas estão em andamento
                
                DisciplinaMatriculada.objects.create(
                    matricula=matricula,
                    codigo=codigo,
                    nome=nome,
                    creditos=creditos,
                    professor=professores.get(nome, 'Professor Desconhecido'),
                    status=status
                )
            
            # Criar matrícula para semestre anterior com disciplinas concluídas
            semestre_anterior = '2022.2'
            
            matricula_anterior = Matricula.objects.create(
                aluno=aluno,
                semestre=semestre_anterior,
                data_matricula=date.today() - timedelta(days=random.randint(180, 240))
            )
            
            # Escolher aleatoriamente entre 4 e 6 disciplinas
            disciplinas_aluno = random.sample(disciplinas_curso, min(num_disciplinas, len(disciplinas_curso)))
            
            # Criar disciplinas matriculadas com status concluído
            for codigo, nome, creditos in disciplinas_aluno:
                # 70% aprovado, 20% reprovado, 10% trancado
                status = random.choices(['APROVADO', 'REPROVADO', 'TRANCADO'], weights=[0.7, 0.2, 0.1])[0]
                
                DisciplinaMatriculada.objects.create(
                    matricula=matricula_anterior,
                    codigo=codigo,
                    nome=nome,
                    creditos=creditos,
                    professor=professores.get(nome, 'Professor Desconhecido'),
                    status=status
                )
        
        self.stdout.write(self.style.SUCCESS(f'Criadas {Matricula.objects.count()} matrículas'))
        self.stdout.write(self.style.SUCCESS(f'Criadas {DisciplinaMatriculada.objects.count()} disciplinas matriculadas'))
    
    def criar_historico_chat(self):
        self.stdout.write('Criando histórico de chat...')
        
        perguntas = [
            "Qual é o horário da disciplina de Banco de Dados?",
            "Qual foi minha nota na prova de Cálculo?",
            "Quando é o vencimento da próxima mensalidade?",
            "Quais disciplinas estou matriculado este semestre?",
            "Qual é o meu índice de frequência na disciplina de Programação?",
            "Quem é o professor de Sistemas Operacionais?",
            "Quando será a próxima prova de Algoritmos?",
            "Como está meu histórico acadêmico?",
            "Quais são os pré-requisitos para a disciplina de IA?",
            "Qual é o procedimento para solicitar trancamento de disciplina?"
        ]
        
        respostas = [
            "Suas aulas de Banco de Dados são às terças-feiras, das 19:00 às 21:00, na sala B201.",
            "Sua nota na prova de Cálculo foi 7.5. A média da turma foi 6.8.",
            "A próxima mensalidade vence em 10/05/2023, no valor de R$ 850,00.",
            "Neste semestre você está matriculado nas disciplinas: Algoritmos, Banco de Dados, Cálculo I e Programação Orientada a Objetos.",
            "Seu índice de frequência na disciplina de Programação é de 85%. O mínimo exigido é 75%.",
            "O professor de Sistemas Operacionais é o Dr. Costa.",
            "A próxima prova de Algoritmos está marcada para 15/06/2023.",
            "Seu histórico acadêmico mostra que você obteve aprovação em 12 disciplinas, com média geral 7.9.",
            "Os pré-requisitos para a disciplina de IA são: Algoritmos e Estruturas de Dados II e Estatística.",
            "Para solicitar trancamento de disciplina, você deve preencher o formulário disponível no portal do aluno até o dia 30/04/2023."
        ]
        
        alunos = Aluno.objects.all()
        
        # Para cada aluno, criar alguns históricos de chat
        for aluno in alunos:
            # Número aleatório de interações (entre 3 e 10)
            num_interacoes = random.randint(3, 10)
            
            for _ in range(num_interacoes):
                # Escolher uma pergunta e resposta aleatória
                idx = random.randint(0, len(perguntas) - 1)
                pergunta = perguntas[idx]
                resposta = respostas[idx]
                
                # Timestamp aleatório nos últimos 30 dias
                minutos_atras = random.randint(1, 30 * 24 * 60)  # até 30 dias atrás em minutos
                timestamp = timezone.now() - timedelta(minutes=minutos_atras)
                
                # Dados contextuais fictícios
                dados_contextuais = {
                    "intenção": random.choice(["consulta_horario", "consulta_nota", "consulta_financeiro", "consulta_matricula"]),
                    "confiança": round(random.uniform(0.7, 0.99), 2),
                    "entidades_identificadas": random.randint(1, 3)
                }
                
                ChatHistorico.objects.create(
                    aluno=aluno,
                    pergunta=pergunta,
                    resposta=resposta,
                    timestamp=timestamp,
                    dados_contextuais=dados_contextuais
                )
        
        self.stdout.write(self.style.SUCCESS(f'Criados {ChatHistorico.objects.count()} registros de histórico de chat')) 