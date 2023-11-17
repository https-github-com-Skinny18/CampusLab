from django.db import models
from django.utils import timezone
import tempfile



class Marca(models.Model):
    nome_marca=models.CharField(null=False,max_length=30, verbose_name='nome da marca do equipamento')

class Equipamento(models.Model):
    nome_equipamento= models.CharField(null=False,max_length=50, verbose_name='nome do equipamento')

class RegimentoInterno(models.Model):
    laboratorio = models.ForeignKey('Laboratorio', on_delete=models.CASCADE, related_name='regimentos_internos')
    pdf = models.FileField(upload_to='pdf_regimentos_internos/')
    nome_do_pdf = models.CharField(max_length=255, default="pedro")
    status = models.BooleanField(default=True)  
    
    def __str__(self):
        return f'Regimento Interno {self.id}'

class UnidadeAcademica(models.Model):
    laboratorio = models.ForeignKey('Laboratorio', on_delete=models.CASCADE, related_name='unidades_academicas_do_laboratorio')
    pdf = models.FileField(upload_to='pdf_unidades_academicas/', null=True, blank=True)

    def __str__(self):
        return f"Unidade Acadêmica para {self.laboratorio}"
    db_table = 'laboratorio'

class ImagemLaboratorio(models.Model):
    imagem = models.ImageField(upload_to='imagens_laboratorio/', null=True, verbose_name='Imagem do Laboratório')
    laboratorios = models.ManyToManyField('Laboratorio', blank=True, related_name='imagens_lab')
    data_upload = models.DateTimeField(default=timezone.now)  # Defina um valor padrão aqui
    def __str__(self):
        return f'Imagem {self.id}'

    def __str__(self):
        return f'Imagem {self.id}'
    
class GrupoDePesquisa(models.Model):
    nome_do_grupo = models.CharField(max_length=50,null=True, verbose_name='Nome do grupo de pesquisa')
    area = models.CharField(max_length=50, null=True, verbose_name='Área de atuação')
    link_grupo = models.URLField(verbose_name='Link do grupo de pesquisa', blank=True, null=True)

    def __str__(self):
        return self.nome_do_grupo

class Laboratorio(models.Model):

    nome_laboratorio = models.CharField(max_length=80, null=False, verbose_name="nome do laboratorio")
    responsavel = models.CharField(null=False,max_length=40,default="jose carlos", verbose_name='Usuário de cadastro')
    email = models.EmailField(verbose_name='email', null=False,default="meu_email@example.com")
    telefone = models.CharField(max_length=15,default="9299999",null=False,verbose_name='numero de telefone')
    unidade = models.CharField(null=True,max_length=10, verbose_name='unidade academica' , default="meu_email")
    rua = models.CharField(null=True, max_length=50,verbose_name='nome da rua do laboratorio' , default="meu_email@example.com")
    numero_rua = models.PositiveIntegerField(null=True,default="32232",verbose_name='numero da rua do laboratorio')
    cep = models.PositiveIntegerField(null=True,default="33323",verbose_name='cep do bairro do laboratorio')
    bairro= models.CharField(null=True, max_length=50,default="jose carlos", verbose_name='nome do bairro do laboratorio')
    andar = models.PositiveIntegerField(null=True, verbose_name='andar do laboratorio')
    sala = models.CharField(null=True, max_length=10, verbose_name='sala do laboratorio')
    apresentacao= models.TextField(null=True,max_length=400,default="jose carlos", verbose_name='Apresentação geral do laboratório:')
    objetivos = models.TextField(null=True,max_length=400, default="jose carlos",verbose_name='Objetivos do laboratório:')
    descricao = models.TextField(null=True, max_length=400, default="ou", verbose_name='descricao das atividades de pesquisa e ensino:')

    link_pnipe = models.CharField(null=True,default="ou",max_length=50, verbose_name='link do pnipe')
    ato_anexo = models.BinaryField(null=True, verbose_name='Anexo do Ato', blank=True)
    unidades_academicas = models.ManyToManyField(UnidadeAcademica, related_name='laboratorios', blank=True)
    imagens = models.ManyToManyField(ImagemLaboratorio, related_name='laboratorios_lab', blank=True)
    grupos_de_pesquisa = models.ManyToManyField(GrupoDePesquisa, related_name='laboratorios', blank=True)


class MembroLaboratorio(models.Model):

    nome_membro = models.CharField(max_length=80, null=True, verbose_name="nome do membro")
    funcao = models.CharField(max_length=40, null=True, verbose_name="função")
    curriculo_lattes = models.URLField(null=True, verbose_name="currículo Lattes")
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE, related_name="membros")

    def __str__(self):
        return self.nome_membro


class Infraestrutura(models.Model):
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE, null=True, default=None)
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE, null=True, related_name='infraestrutura_equipamento', verbose_name='Nome do Equipamento lista')
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, null=True, related_name='infraestrutura_marca', verbose_name='Nome da Marca lista')
    modelo = models.CharField(null=True, max_length=30, verbose_name='modelo do equipamento')
    finalidade = models.CharField(null=True, max_length=300, verbose_name='finalidade do equipamento')
    status = models.BooleanField(default=True)  
    tombo =  models.CharField(null=True,default='-', max_length=300, verbose_name='tombo')
    quantidade = models.PositiveIntegerField(default=0)

class ImagemInfraestrutura(models.Model):
    imagem = models.ImageField(upload_to='infraestrutura_images/', null=True, blank=True, verbose_name='Imagem da Infraestrutura')
    infraestrutura = models.ForeignKey(Infraestrutura, on_delete=models.CASCADE, related_name='imagens_infraestrutura', verbose_name='Infraestrutura')

    def __str__(self):
        return f'Imagem da Infraestrutura #{self.id}'
    def __str__(self):
        return f"Infraestrutura #{self.id}"
    

    


class LaboratorioInfraestrutura(models.Model):
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE, related_name='infraestruturas')
    infraestrutura = models.ForeignKey(Infraestrutura, on_delete=models.CASCADE)


class Projeto(models.Model):
    projeto = models.CharField(max_length=255, default=1)
    nome_projeto = models.CharField(max_length=255)
    docente_responsavel = models.CharField(max_length=255)
    discente_participante = models.CharField(max_length=255)
    matricula_discente = models.CharField(max_length=50, blank=True, null=True)  # Permite valores nulos
    modalidade = models.CharField(max_length=100)
    vigencia_inicio = models.DateField()
    vigencia_fim = models.DateField()
    fomento = models.CharField(max_length=100)
    laboratorio = models.ForeignKey('Laboratorio', on_delete=models.CASCADE, default=1, related_name='projetos_lab')

    def __str__(self):
        return self.projeto

   


    
# class Grupo(models.Model):
#    nome_do_grupo = models.CharField(null=True,max_length=50, verbose_name='Nome do grupo de pesquisa')
#    area = models.CharField(null=False,max_length=50, verbose_name='area de atuacao')
#    ano_de_criacao = models.DateField(null=True, verbose_name='Data de criação do grupo de pesquisa')

 
# class Projeto(models.Model):
#     nome_do_projeto= models.CharField(null=False,max_length=50, verbose_name='nome do projeto')
#     responsavel_projeto= models.CharField(null=False,max_length=50, verbose_name='responsavel pelo projeto')
#     nome_discente=models.CharField(null=False,max_length=50, verbose_name='aluno no projeto')
#     matricula_discente=models.PositiveIntegerField(null=False,verbose_name='numero da matricula do aluno')
#     modalidade=models.CharField(null=False,max_length=50, verbose_name='modalidades da pesquisa')
#     inicio_projeto= models.DateField(null=True, verbose_name='Data de inicio do projeto ')
#     fim_projeto=models.DateField(null=True, verbose_name='Data do fim do projeto')
#     formento= models.CharField(null=False,max_length=50, verbose_name='apoio ao projeto')

class Unidade(models.Model):
    Unidade = models.CharField(max_length=100)  # Adicione este campo para armazenar o setor do usuário

    class Meta:
        managed = False
        db_table = 'XPROJ2.UNIDADE'
