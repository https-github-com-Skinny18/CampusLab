# Generated by Django 4.1.3 on 2023-11-17 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_regimentointerno_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='infraestrutura',
            name='tombo',
            field=models.CharField(max_length=300, null=True, verbose_name='tombo'),
        ),
    ]
