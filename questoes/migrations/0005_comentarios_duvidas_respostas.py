# Generated by Django 5.0.2 on 2024-03-04 12:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questoes', '0004_alter_questao_estado'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(default='', max_length=5000, verbose_name='Texto')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data')),
                ('visibilidade', models.BooleanField(default=True, verbose_name='Visibilidade')),
                ('questao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questoes.questao', verbose_name='Questão')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Comentario',
                'verbose_name_plural': 'Comentarios',
            },
        ),
        migrations.CreateModel(
            name='Duvidas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(default='', max_length=5000, verbose_name='Texto')),
                ('arquivo', models.FileField(blank=True, default=None, null=True, upload_to='duvidas/%Y/%m/%d/', verbose_name='Arquivo')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data')),
                ('visibilidade', models.BooleanField(default=True, verbose_name='Visibilidade')),
                ('questao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questoes.questao', verbose_name='Questão')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Duvida',
                'verbose_name_plural': 'Duvidas',
            },
        ),
        migrations.CreateModel(
            name='Respostas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(default='', max_length=5000, verbose_name='Texto')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data')),
                ('visibilidade', models.BooleanField(default=True, verbose_name='Visibilidade')),
                ('duvida', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='questoes.duvidas', verbose_name='Dúvida')),
            ],
            options={
                'verbose_name': 'Resposta',
                'verbose_name_plural': 'Respostas',
            },
        ),
    ]
