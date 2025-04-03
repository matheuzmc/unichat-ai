from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'alunos', views.AlunoViewSet)
router.register(r'notas', views.NotaViewSet)
router.register(r'horarios', views.HorarioAulaViewSet)
router.register(r'frequencias', views.FrequenciaViewSet)
router.register(r'financeiro', views.DadoFinanceiroViewSet)
router.register(r'matriculas', views.MatriculaViewSet)
router.register(r'disciplinas-matriculadas', views.DisciplinaMatriculadaViewSet)
router.register(r'chat-historico', views.ChatHistoricoViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 