# Generated by Django 5.0.2 on 2024-02-27 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_post_titulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='', max_length=1100, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='post',
            name='titulo',
            field=models.CharField(default='', max_length=1000, verbose_name='Título'),
        ),
    ]
