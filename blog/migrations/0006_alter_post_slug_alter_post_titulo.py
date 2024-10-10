# Generated by Django 5.0.2 on 2024-02-27 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_post_descricao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='', max_length=1100, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='post',
            name='titulo',
            field=models.CharField(default='', max_length=1000, unique=True, verbose_name='Título'),
        ),
    ]
