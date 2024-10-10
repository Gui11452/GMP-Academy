from django.db import models
from django.contrib.auth.models import User

class SobreNos(models.Model):
    titulo = models.CharField(max_length=500, verbose_name="Título")
    texto = models.TextField(max_length=1000000000, verbose_name="Texto")
    video = models.FileField(upload_to="sobre_nos/%Y/%m/%d/", verbose_name='Vídeo')
    foto = models.FileField(upload_to="sobre_nos/%Y/%m/%d/", verbose_name='Capa', blank=True, null=True)

    class Meta:
        verbose_name = 'Sobre Nós'
        verbose_name_plural = 'Sobre Nós'

    def __str__(self):
        return f'{self.titulo}'
    

class FaleConosco(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    data = models.DateTimeField(auto_now=True, verbose_name="Data", blank=True, null=True)
    titulo = models.CharField(max_length=500, verbose_name="Título")
    assunto = models.CharField(max_length=1000000000, verbose_name="Assunto")
    texto = models.TextField(verbose_name="Texto")

    class Meta:
        verbose_name = 'Fale Conosco'
        verbose_name_plural = 'Fale Conosco'

    def __str__(self):
        return f'{self.titulo}'
    

class ArquivosExcel(models.Model):
    arquivo = models.FileField(upload_to="uploads/%Y/%m/%d/")

    class Meta:
        verbose_name = 'Arquivo Excel'
        verbose_name_plural = 'Arquivos Excel'

    def __str__(self):
        return f'{self.arquivo.url}'
    

class EmailsProntos(models.Model):
    titulo = models.CharField(max_length=1000, verbose_name="Título")
    texto1 = models.TextField(verbose_name="Texto1", blank=True, null=True)
    texto2 = models.TextField(verbose_name="Texto2", blank=True, null=True)
    texto3 = models.TextField(verbose_name="Texto3", blank=True, null=True)
    texto4 = models.TextField(verbose_name="Texto4", blank=True, null=True)
    texto5 = models.TextField(verbose_name="Texto5", blank=True, null=True)
    texto6 = models.TextField(verbose_name="Texto6", blank=True, null=True)
    texto7 = models.TextField(verbose_name="Texto7", blank=True, null=True)
    texto8 = models.TextField(verbose_name="Texto8", blank=True, null=True)
    contagem = models.IntegerField(default=0, verbose_name='Contagem')

    class Meta:
        verbose_name = 'Email Pronto'
        verbose_name_plural = 'Emails Prontos'

    def __str__(self):
        return f'{self.titulo}'
