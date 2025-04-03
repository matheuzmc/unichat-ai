from django.contrib import admin
from .models import (
    Aluno, Nota, HorarioAula, Frequencia, DadoFinanceiro, 
    Matricula, DisciplinaMatriculada, ChatHistorico
)

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'email', 'curso', 'semestre')
    search_fields = ('nome', 'matricula', 'email')
    list_filter = ('curso', 'semestre')

@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'disciplina', 'nota_final', 'data_avaliacao', 'semestre')
    search_fields = ('aluno__nome', 'disciplina')
    list_filter = ('semestre', 'data_avaliacao')

@admin.register(HorarioAula)
class HorarioAulaAdmin(admin.ModelAdmin):
    list_display = ('disciplina', 'aluno', 'dia_semana', 'horario_inicio', 'horario_fim', 'sala')
    search_fields = ('disciplina', 'aluno__nome', 'professor')
    list_filter = ('dia_semana', 'semestre')

@admin.register(Frequencia)
class FrequenciaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'disciplina', 'data', 'status')
    search_fields = ('aluno__nome', 'disciplina')
    list_filter = ('status', 'data')

@admin.register(DadoFinanceiro)
class DadoFinanceiroAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'descricao', 'mensalidade', 'data_vencimento', 'status_pagamento')
    search_fields = ('aluno__nome', 'descricao')
    list_filter = ('status_pagamento', 'data_vencimento')

@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'semestre', 'data_matricula')
    search_fields = ('aluno__nome', 'semestre')
    list_filter = ('semestre',)

@admin.register(DisciplinaMatriculada)
class DisciplinaMatriculadaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'professor', 'creditos', 'status')
    search_fields = ('codigo', 'nome', 'professor')
    list_filter = ('status', 'creditos')

@admin.register(ChatHistorico)
class ChatHistoricoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'pergunta', 'timestamp')
    search_fields = ('aluno__nome', 'pergunta', 'resposta')
    list_filter = ('timestamp',)
    readonly_fields = ('timestamp',)
