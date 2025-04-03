from django.core.management.base import BaseCommand
from api.models import (
    Aluno, Nota, HorarioAula, Frequencia, DadoFinanceiro, 
    Matricula, DisciplinaMatriculada, ChatHistorico
)

class Command(BaseCommand):
    help = 'Limpa todos os dados do banco de dados'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando limpeza do banco de dados...'))
        
        # Excluir na ordem reversa das dependências de chave estrangeira
        self.stdout.write('Excluindo registros de ChatHistorico...')
        ChatHistorico.objects.all().delete()
        
        self.stdout.write('Excluindo registros de DisciplinaMatriculada...')
        DisciplinaMatriculada.objects.all().delete()
        
        self.stdout.write('Excluindo registros de Matricula...')
        Matricula.objects.all().delete()
        
        self.stdout.write('Excluindo registros de DadoFinanceiro...')
        DadoFinanceiro.objects.all().delete()
        
        self.stdout.write('Excluindo registros de Frequencia...')
        Frequencia.objects.all().delete()
        
        self.stdout.write('Excluindo registros de HorarioAula...')
        HorarioAula.objects.all().delete()
        
        self.stdout.write('Excluindo registros de Nota...')
        Nota.objects.all().delete()
        
        self.stdout.write('Excluindo registros de Aluno...')
        Aluno.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Limpeza do banco de dados concluída com sucesso!')) 