from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    verificacao_email = models.BooleanField(default=False, verbose_name='Verificação')
    codigo = models.CharField(max_length=255, default='', verbose_name='Código')
    foto = models.FileField(upload_to="fotos_perfis/%Y/%m/%d/", verbose_name="Foto", default=None, blank=True, null=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return f'{self.usuario}'
    
class RecuperacaoSenha(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    recuperacao = models.BooleanField(default=False, verbose_name='Foi Recuperado?')
    codigo = models.CharField(max_length=255, default='', verbose_name='Código')
    data = models.DateTimeField(default=timezone.now, verbose_name='Data')

    class Meta:
        verbose_name = 'Recuperação de Senha'
        verbose_name_plural = 'Recuperação de Senhas'

    def __str__(self):
        return f'{self.usuario}'


# Pedidos e Planos - Início

class Planos(models.Model):
    preco = models.FloatField(default=0, verbose_name="Preco")
    nome = models.CharField(default='', verbose_name="Nome", max_length=255)
    tipo = models.CharField(
		default='basico',
		max_length=100,
		choices=(
            ('basico', 'basico'),
            ('avancado', 'avancado'),
            ('intermediario', 'intermediario'),
        ),
		verbose_name="Tipo de Plano"
	)

    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'

    def __str__(self):
        return f'{self.nome} -> {self.preco}'
    
class Topicos(models.Model):
    nome = models.CharField(default='', verbose_name="Nome", max_length=1000)
    plano = models.ForeignKey(Planos, on_delete=models.CASCADE, verbose_name='Planos', default=None, null=True, blank=True)

    class Meta:
        verbose_name = 'Topico'
        verbose_name_plural = 'Topicos'

    def __str__(self):
        return f'{self.nome}'


class Pedido(models.Model):
    comprador = models.ForeignKey(Perfil, on_delete=models.SET_NULL, 
                                          verbose_name="Comprador", blank=True, null=True)
    
    metodo_pagamento = models.CharField(
		default='UNDEFINED',
		max_length=20,
		choices=(
            ('UNDEFINED', 'UNDEFINED'),
			('CREDIT_CARD', 'CREDIT_CARD'),
			('PIX', 'PIX'),
            ('BOLETO', 'BOLETO'),
		), 
		verbose_name="Método de Pagamento",
	)

    preco_pedido = models.FloatField(default=0, verbose_name="Preço do pedido")
    data_pedido = models.DateTimeField(auto_now=True, verbose_name="Data do pedido")
    data_ultima_atualizacao = models.DateTimeField(auto_now_add=True, verbose_name="Data da Última Atualização", blank=True, null=True)

    link_pagamento = models.URLField(default='', max_length=1000, verbose_name='Link de Pagamento')

    descricao_pagamento = models.CharField(default='', max_length=500, verbose_name="Descrição do pagamento", blank=True, null=True)
    plano = models.CharField(
		default='basico',
		max_length=20,
		choices=(
			('basico', 'basico'),
			('intermediario', 'intermediario'),
            ('avancado', 'avancado'),
		), 
		verbose_name="Plano Escolhido",
	)
    status_pedido = models.CharField(
		default='pending',
		max_length=20,
		choices=(
			('approved', 'approved'),
			('rejected', 'rejected'),
            ('pending', 'pending'),
		), 
		verbose_name="Status Pedido",
	)

    idPagamento = models.CharField(default='', max_length=255, verbose_name="idPagamento")
    idAssinatura = models.CharField(default='', max_length=255, verbose_name="idAssinatura")
    customer = models.CharField(default='', max_length=255, verbose_name="Customer")
    endDate = models.CharField(default='', max_length=255, verbose_name="Data de Vencimento do Link")
    
    plano_ativo = models.BooleanField(default=False, verbose_name="Plano Ativo")

    recebeu_email_aprovado = models.BooleanField(default=False, verbose_name="Código Interno AP")
    recebeu_email_reprovado = models.BooleanField(default=False, verbose_name="Código Interno REP")
    recebeu_email_pendente = models.BooleanField(default=False, verbose_name="Código Interno PEN")

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return f'{self.comprador} -> {self.id}'
# Pedidos e Planos - Fim