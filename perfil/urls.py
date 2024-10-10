from django.urls import path
from . import views

urlpatterns = [
    path('', views.perfil, name='perfil'),
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout, name='logout'),
    path('confirmacao_email/<str:codigo>/', views.confirmar_email, name='confirmar_email'),
    path('pedir_confirmacao_email/', views.pedir_confirmacao_email, name='pedir_confirmacao_email'),
    path('esqueceu_senha/', views.esqueceu_senha, name='esqueceu_senha'),
    path('alterar_dados/', views.alterar_dados, name='alterar_dados'),
    path('recuperacao_senha/<str:codigo>/', views.recuperacao_senha, name='recuperacao_senha'),

    # Gerenciamento e Pagamento Assinaturas - Início
    path('escolher_plano/<str:plano>/', views.escolher_plano, name='escolher_plano'),
    path('registro_pagamento/<str:situation>/', views.registro_pagamento, name='registro_pagamento'),
    path('payment/', views.payment, name='payment'),
    path('sucesso/', views.sucesso, name='sucesso'),
    path('rejeitado/', views.rejeitado, name='rejeitado'),
    path('atualizar_assinatura/', views.atualizar_assinatura, name='atualizar_assinatura'),

    path('webhook/', views.webhook, name='webhook'),
    # Gerenciamento e Pagamento Assinaturas - Fim
]