from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('planos/', views.planos, name='planos'),
    path('quem_somos/', views.quem_somos, name='quem_somos'),
    path('fale_conosco/', views.fale_conosco, name='fale_conosco'),
    path('envio_emails/', views.envio_emails, name='envio_emails'),
    path('cadastro_questoes/', views.cadastro_questoes, name='cadastro_questoes'),
]