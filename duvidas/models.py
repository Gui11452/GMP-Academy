from django.db import models
from django.contrib.auth.models import User
from questoes.models import Questao

# Comentários e Dúvidas - Início
class Comentarios(models.Model):
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, verbose_name="Questão")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    texto = models.TextField(default='', max_length=5000, verbose_name="Texto")
    data = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    visibilidade = models.BooleanField(default=True, verbose_name="Visibilidade")

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        return f'{self.usuario}'
    

class Duvidas(models.Model):
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, verbose_name="Questão")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    texto = models.TextField(default='', max_length=5000, verbose_name="Texto")
    arquivo = models.FileField(upload_to="duvidas/%Y/%m/%d/", verbose_name="Arquivo", default=None, blank=True, null=True)
    data = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    visibilidade = models.BooleanField(default=True, verbose_name="Visibilidade")

    class Meta:
        verbose_name = 'Duvida'
        verbose_name_plural = 'Duvidas'

    def __str__(self):
        return f'{self.texto}'
    
class ReportarDuvidasProfessor(models.Model):
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, verbose_name="Questão")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    texto = models.TextField(default='', max_length=5000, verbose_name="Texto")
    arquivo = models.FileField(upload_to="reportar_duvidas_professor/%Y/%m/%d/", verbose_name="Arquivo", default=None, blank=True, null=True)
    data = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    visibilidade = models.BooleanField(default=True, verbose_name="Visibilidade")

    class Meta:
        verbose_name = 'Reportar Duvida Professor'
        verbose_name_plural = 'Reportar Duvidas Professor'

    def __str__(self):
        return f'{self.texto}'
    

class Respostas(models.Model):
    duvida = models.OneToOneField(Duvidas, on_delete=models.CASCADE, verbose_name="Dúvida")
    texto = models.TextField(default='', max_length=5000, verbose_name="Texto")
    data = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    visibilidade = models.BooleanField(default=True, verbose_name="Visibilidade")

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'

    def __str__(self):
        return f'{self.id}'
# Comentários e Dúvidas - Fim
