# Generated by Django 5.0.2 on 2024-03-31 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questoes', '0006_reportarduvidasprofessor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='duvidas',
            name='questao',
        ),
        migrations.RemoveField(
            model_name='duvidas',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='respostas',
            name='duvida',
        ),
        migrations.RemoveField(
            model_name='reportarduvidasprofessor',
            name='questao',
        ),
        migrations.RemoveField(
            model_name='reportarduvidasprofessor',
            name='usuario',
        ),
        migrations.DeleteModel(
            name='Comentarios',
        ),
        migrations.DeleteModel(
            name='Duvidas',
        ),
        migrations.DeleteModel(
            name='Respostas',
        ),
        migrations.DeleteModel(
            name='ReportarDuvidasProfessor',
        ),
    ]
