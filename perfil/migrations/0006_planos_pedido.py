# Generated by Django 5.0.2 on 2024-02-27 03:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0005_alter_recuperacaosenha_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Planos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basico', models.FloatField(default=0, verbose_name='Plano Básico')),
                ('intermediario', models.FloatField(default=0, verbose_name='Plano Intermediário')),
                ('avancado', models.FloatField(default=0, verbose_name='Plano Avançado')),
            ],
            options={
                'verbose_name': 'Plano',
                'verbose_name_plural': 'Planos',
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metodo_pagamento', models.CharField(choices=[('CREDIT_CARD', 'CREDIT_CARD'), ('PIX', 'PIX'), ('BOLETO', 'BOLETO')], default='CREDIT_CARD', max_length=20, verbose_name='Método de Pagamento')),
                ('preco_pedido', models.FloatField(default=0, verbose_name='Preço do pedido')),
                ('data_pedido', models.DateTimeField(auto_now_add=True, verbose_name='Data do pedido')),
                ('data_vencimento', models.DateTimeField(blank=True, null=True, verbose_name='Data do vencimento')),
                ('descricao_pagamento', models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='Descrição do pagamento')),
                ('plano', models.CharField(choices=[('basico', 'basico'), ('intermediario', 'intermediario'), ('avancado', 'avancado')], default='basico', max_length=20, verbose_name='Plano Escolhido')),
                ('status_pedido', models.CharField(choices=[('approved', 'approved'), ('rejected', 'rejected'), ('pending', 'pending')], default='pending', max_length=20, verbose_name='Status Pedido')),
                ('idPlano', models.CharField(default='', max_length=255, verbose_name='idPlano')),
                ('customer', models.CharField(default='', max_length=255, verbose_name='Customer')),
                ('url_payment', models.URLField(default='', max_length=1000, verbose_name='Link Pagamento')),
                ('endDate', models.CharField(default='', max_length=255, verbose_name='Data de Vencimento do Link')),
                ('plano_ativo', models.BooleanField(default=False, verbose_name='Plano Ativo')),
                ('recebeu_email_aprovado', models.BooleanField(default=False, verbose_name='Código Interno AP')),
                ('recebeu_email_reprovado', models.BooleanField(default=False, verbose_name='Código Interno REP')),
                ('recebeu_email_pendente', models.BooleanField(default=False, verbose_name='Código Interno PEN')),
                ('comprador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='perfil.perfil', verbose_name='Comprador')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
            },
        ),
    ]
