from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Aluno(models.Model):
    """
    Modelo para armazenar informações pessoais e acadêmicas dos alunos.
    """
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    matricula = models.CharField(max_length=20, unique=True)
    curso = models.CharField(max_length=255)
    semestre = models.PositiveSmallIntegerField()
    data_nascimento = models.DateField()
    endereco = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} - {self.matricula}"

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
        ordering = ['nome']


class Nota(models.Model):
    """
    Modelo para armazenar as notas dos alunos nas disciplinas.
    """
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='notas')
    disciplina = models.CharField(max_length=255)
    nota_prova = models.DecimalField(
        max_digits=4, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    nota_trabalho = models.DecimalField(
        max_digits=4, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    nota_final = models.DecimalField(
        max_digits=4, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    data_avaliacao = models.DateField()
    semestre = models.CharField(max_length=10)  # Ex: "2023.1"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.aluno.nome} - {self.disciplina} - {self.nota_final}"

    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Notas"
        ordering = ['-data_avaliacao']


class HorarioAula(models.Model):
    """
    Modelo para armazenar os horários de aulas dos alunos.
    """
    DIAS_SEMANA = [
        ('SEG', 'Segunda-feira'),
        ('TER', 'Terça-feira'),
        ('QUA', 'Quarta-feira'),
        ('QUI', 'Quinta-feira'),
        ('SEX', 'Sexta-feira'),
        ('SAB', 'Sábado'),
        ('DOM', 'Domingo'),
    ]

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='horarios')
    disciplina = models.CharField(max_length=255)
    dia_semana = models.CharField(max_length=3, choices=DIAS_SEMANA)
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    sala = models.CharField(max_length=255)
    professor = models.CharField(max_length=255)
    semestre = models.CharField(max_length=10)  # Ex: "2023.1"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.disciplina} - {self.get_dia_semana_display()} - {self.horario_inicio}"

    class Meta:
        verbose_name = "Horário de Aula"
        verbose_name_plural = "Horários de Aulas"
        ordering = ['dia_semana', 'horario_inicio']


class Frequencia(models.Model):
    """
    Modelo para armazenar a frequência dos alunos nas disciplinas.
    """
    STATUS_CHOICES = [
        ('PRESENTE', 'Presente'),
        ('AUSENTE', 'Ausente'),
        ('JUSTIFICADO', 'Justificado'),
    ]

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='frequencias')
    disciplina = models.CharField(max_length=255)
    data = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.aluno.nome} - {self.disciplina} - {self.data} - {self.status}"

    class Meta:
        verbose_name = "Frequência"
        verbose_name_plural = "Frequências"
        ordering = ['-data']


class DadoFinanceiro(models.Model):
    """
    Modelo para armazenar informações financeiras dos alunos.
    """
    STATUS_CHOICES = [
        ('PAGO', 'Pago'),
        ('PENDENTE', 'Pendente'),
        ('ATRASADO', 'Atrasado'),
        ('ISENTO', 'Isento'),
    ]

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='dados_financeiros')
    mensalidade = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    status_pagamento = models.CharField(max_length=10, choices=STATUS_CHOICES)
    data_pagamento = models.DateField(null=True, blank=True)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    descricao = models.CharField(max_length=255, default="Mensalidade")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.aluno.nome} - {self.descricao} - {self.data_vencimento} - {self.status_pagamento}"

    class Meta:
        verbose_name = "Dado Financeiro"
        verbose_name_plural = "Dados Financeiros"
        ordering = ['-data_vencimento']


class Matricula(models.Model):
    """
    Modelo para armazenar as matrículas dos alunos nas disciplinas.
    """
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='matriculas')
    semestre = models.CharField(max_length=10)  # Ex: "2023.1"
    data_matricula = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.aluno.nome} - {self.semestre}"

    class Meta:
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"
        ordering = ['-semestre']


class DisciplinaMatriculada(models.Model):
    """
    Modelo para armazenar as disciplinas em que um aluno está matriculado.
    """
    STATUS_CHOICES = [
        ('EM_ANDAMENTO', 'Em andamento'),
        ('APROVADO', 'Aprovado'),
        ('REPROVADO', 'Reprovado'),
        ('TRANCADO', 'Trancado'),
    ]

    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE, related_name='disciplinas')
    codigo = models.CharField(max_length=20)
    nome = models.CharField(max_length=255)
    creditos = models.PositiveSmallIntegerField()
    professor = models.CharField(max_length=255)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='EM_ANDAMENTO')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.codigo} - {self.nome} - {self.status}"

    class Meta:
        verbose_name = "Disciplina Matriculada"
        verbose_name_plural = "Disciplinas Matriculadas"
        ordering = ['nome']


class ChatHistorico(models.Model):
    """
    Modelo para armazenar o histórico de perguntas e respostas do chat.
    """
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='historico_chat')
    pergunta = models.TextField()
    resposta = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    dados_contextuais = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.aluno.nome} - {self.timestamp}"

    class Meta:
        verbose_name = "Histórico de Chat"
        verbose_name_plural = "Históricos de Chat"
        ordering = ['-timestamp']
