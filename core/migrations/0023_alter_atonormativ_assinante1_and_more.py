# Generated by Django 4.1.3 on 2023-03-30 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_autoridade_alter_atonormativ_autoridade1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atonormativ',
            name='assinante1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ato_normativ_autoridade1', to='core.autoridade', verbose_name='Autoridade 1'),
        ),
        migrations.AlterField(
            model_name='atonormativ',
            name='autoridade1',
            field=models.CharField(default='setor', max_length=45, null=True, verbose_name='Autoridade 2'),
        ),
    ]
