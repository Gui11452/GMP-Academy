# Generated by Django 5.0.2 on 2024-03-31 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0018_remove_planos_topicos_topicos_plano'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planos',
            name='avancado',
        ),
        migrations.RemoveField(
            model_name='planos',
            name='basico',
        ),
        migrations.RemoveField(
            model_name='planos',
            name='intermediario',
        ),
        migrations.RemoveField(
            model_name='planos',
            name='nome_plano_avancado',
        ),
        migrations.RemoveField(
            model_name='planos',
            name='nome_plano_basico',
        ),
        migrations.RemoveField(
            model_name='planos',
            name='nome_plano_intermediario',
        ),
        migrations.AddField(
            model_name='planos',
            name='nome',
            field=models.CharField(default='', max_length=255, verbose_name='Nome'),
        ),
        migrations.AddField(
            model_name='planos',
            name='preco',
            field=models.FloatField(default=0, verbose_name='Preco'),
        ),
    ]
