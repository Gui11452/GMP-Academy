# Generated by Django 5.0.2 on 2024-03-31 23:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0016_planos_nome_plano_avancado_planos_nome_plano_basico_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topicos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(default='', max_length=1000, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Topico',
                'verbose_name_plural': 'Topicos',
            },
        ),
        migrations.AddField(
            model_name='planos',
            name='topicos',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='perfil.topicos', verbose_name='Topicos'),
        ),
    ]
