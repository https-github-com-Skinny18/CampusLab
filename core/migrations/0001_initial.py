# Generated by Django 4.1.3 on 2023-10-07 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Unidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Unidade', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'XPROJ2.UNIDADE',
                'managed': False,
            },
        ),
    ]
