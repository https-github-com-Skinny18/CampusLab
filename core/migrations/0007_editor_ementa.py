# Generated by Django 4.1.3 on 2023-01-31 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_editor_campo_editor_descricao'),
    ]

    operations = [
        migrations.AddField(
            model_name='editor',
            name='ementa',
            field=models.TextField(blank=True, null=True),
        ),
    ]
