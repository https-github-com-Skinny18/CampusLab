# Generated by Django 4.1.3 on 2023-03-24 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_atonormativo_delete_core_atonormativo'),
    ]

    operations = [
        migrations.CreateModel(
            name='core_atonormativo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomemo', models.TextField(blank=True, null=True)),
            ],
        ),
    ]