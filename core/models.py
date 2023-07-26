from django.db import models
from tinymce.models import HTMLField
from django.utils import timezone
import datetime
from django.utils.html import strip_tags
import pytz


class Composicao (models.Model):
    # composicao_id = models.AutoField(primary_key=True)
    usario = models.CharField(max_length=80,verbose_name='Usuario')
    sigla_setor = models.CharField(max_length=20,verbose_name='sigla do setor')
    nome_setor = models.CharField(max_length=80,verbose_name= 'nome do setor')
    tipo_ato = models.CharField(max_length=10, choices=[('portaria', 'Portaria'), ('resolucao', 'Resolução'), ('boletim', 'Boletim')], verbose_name='Tipo de Ato Normativo')
    # portaria = models.CharField(max_length=1,verbose_name='caso seja uma portaria')
    # resolucao = models.CharField(max_length=1,verbose_name='caso seja uma resolucao')
    # boletim = models.CharField(max_length=1,verbose_name='caso seja uma boletim')
    db_table = 'Composicao'
        


class Autoridade(models.Model):
    nome = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.nome}/{self.id}"
    
class AtoNormativ(models.Model):
    STATUS_CHOICES=[
        ('revisao', 'Revisão'),
        ('aprovado', 'Aprovado'),
        ('pendente', 'Pendente'),
        ('cancelado', 'Cancelado'),
    ]
    
    data = models.DateTimeField(default=timezone.datetime(2000, 10, 10, tzinfo=pytz.timezone('America/Manaus')), verbose_name='Data de criação')
    numero = models.PositiveIntegerField(null=False,unique=True, verbose_name='Número')
    # nao esquecer de que chave era unica abaixo
    ano = models.PositiveIntegerField(null=False, verbose_name='Ano')  
    doe_data = models.DateTimeField(auto_now_add=True, verbose_name='Data do Diário Oficial')
    doe_numero = models.PositiveIntegerField(null=True,verbose_name='Número do Diário Oficial')
    doe_secao = models.CharField(max_length=40, verbose_name='Seção do Diário Oficial')
    doe_pagina = models.CharField(max_length=40, verbose_name='Página do Diário Oficial')
    dt_cadastro = models.DateTimeField(null=False,default=timezone.datetime(2000, 10, 10, tzinfo=pytz.timezone('America/Manaus')),verbose_name='Data de cadastro')
    usr_cadastro = models.CharField(null=False,default='enzo', max_length=40, verbose_name='Usuário de cadastro')
    ementa = models.TextField(max_length=400, verbose_name='Ementa')
    texto_normativo = models.TextField(null=False, default='escrever',max_length=1000, verbose_name='Texto normativo')
    publicado = models.CharField(null=False, default='n',max_length=1, verbose_name='Publicado')
    dt_alteracao= models.DateField(auto_now=True, verbose_name='Data de alteração')
    usr_alteracao = models.CharField(max_length=20, verbose_name='Usuário de alteração')
    dt_publicado = models.DateField(null=True, blank=True, verbose_name='Data de publicação')
    usr_publicacao = models.CharField(max_length=45, verbose_name='Usuário de publicação')
    autoridade1 = models.CharField(max_length=45,null=False,default='setor', verbose_name='Autoridade 1')
    autoridade2 = models.CharField(max_length=45,null=True,default='setor', verbose_name='Autoridade 2')
    assinante1 = models.ForeignKey(Autoridade, on_delete=models.CASCADE, related_name='ato_normativ_assinante1', verbose_name='Assinante 1')
    assinante2 = models.CharField(max_length=45,null=True, verbose_name='Assinante 2')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='revisao')
    # tipo_ato = models.ForeignKey(Composicao, on_delete=models.CASCADE, verbose_name='Tipo de Ato Normativo',
    #                           limit_choices_to={'tipo_ato__in': [('portaria', 'Portaria'), ('resolucao', 'Resolução'), ('boletim', 'Boletim')]}, default=None)
    tipo_ato = models.CharField(max_length=45, null=True, verbose_name='ato')
    db_table = 'AtoNormativ'

    def __str__(self):
        return f"{self.texto_normativo}/{self.ementa}"
    

     
   
