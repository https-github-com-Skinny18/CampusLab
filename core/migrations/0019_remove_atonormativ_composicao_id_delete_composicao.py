# Generated by Django 4.1.3 on 2023-03-27 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_atonormativ_doe_numero'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atonormativ',
            name='composicao_id',
        ),
        migrations.DeleteModel(
            name='Composicao',
        ),
    ]
