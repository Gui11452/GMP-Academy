# Generated by Django 5.0.2 on 2024-05-28 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questoes', '0011_remove_aula_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aula',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='pdfs/%Y/%m/%d/', verbose_name='PDF (Opcional)'),
        ),
    ]
