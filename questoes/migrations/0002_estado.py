# Generated by Django 5.0.2 on 2024-02-27 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questoes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=300, unique=True, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Estado',
                'verbose_name_plural': 'Estados',
            },
        ),
    ]
