# Generated by Django 4.2.2 on 2023-07-06 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_alter_atonormativ_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='atonormativ',
            name='doe_numero_boletim',
            field=models.PositiveIntegerField(null=True, verbose_name='Número do Diário Oficial'),
        ),
    ]
