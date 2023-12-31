# Generated by Django 4.1.3 on 2023-12-06 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_infraestrutura_tombo'),
    ]

    operations = [
        migrations.AddField(
            model_name='laboratorio',
            name='cpf_responsavel',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='user_ldap_responsavel',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='responsavel',
            field=models.CharField(default='jose carlos', max_length=255, verbose_name='Usuário de cadastro'),
        ),
        migrations.CreateModel(
            name='ResponsavelAssociado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome do Responsável Associado')),
                ('cpf', models.CharField(blank=True, max_length=11, null=True, verbose_name='CPF do Responsável Associado')),
                ('user_ldap', models.CharField(blank=True, max_length=255, null=True, verbose_name='USER_LDAP do Responsável Associado')),
                ('laboratorio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsaveis_associados', to='core.laboratorio')),
            ],
        ),
    ]
