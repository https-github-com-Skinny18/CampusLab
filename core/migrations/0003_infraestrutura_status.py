# Generated by Django 4.1.3 on 2023-10-30 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_equipamento_grupodepesquisa_imagemlaboratorio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='infraestrutura',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
