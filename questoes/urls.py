from django.urls import path
from . import views

urlpatterns = [
    path('questoes/', views.questoes, name='questoes'),
    path('responder_questao/<int:id>/', views.responder_questao, name='responder_questao'),

    path('questao/<str:codigo>/', views.questao, name='questao'),
    path('aulas/', views.aulas, name='aulas'),
    
    path('refazer_questao/<int:id>/', views.refazer_questao, name='refazer_questao'),
    path('refazer_questao_2/<int:id>/', views.refazer_questao_2, name='refazer_questao_2'),

    path('enviar_comentario/<int:id>/', views.enviar_comentario, name='enviar_comentario'),
    path('enviar_duvida/<int:id>/', views.enviar_duvida, name='enviar_duvida'),
    path('enviar_duvida_professor/<int:id>/', views.enviar_duvida_professor, name='enviar_duvida_professor'),

    path('redirecionamento_questoes/<str:prova>/', views.redirecionamento_questoes, name='redirecionamento_questoes'),
    path('redirecionamento_questoes_form/', views.redirecionamento_questoes_form, name='redirecionamento_questoes_form'),
    path('redirecionamento_aulas/<str:disciplina>/', views.redirecionamento_aulas, name='redirecionamento_aulas'),
]