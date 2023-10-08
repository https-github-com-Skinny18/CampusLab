from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse

from django.utils.html import strip_tags
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Laboratorio, Infraestrutura,LaboratorioInfraestrutura,ImagemLaboratorio, Marca, Equipamento, RegimentoInterno, UnidadeAcademica,ImagemInfraestrutura,GrupoDePesquisa,MembroLaboratorio
from django.contrib.messages import constants
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from PIL import Image
from datetime import datetime
import io
import base64
from django.core.files.base import ContentFile
import logging
from django.templatetags.static import static
from django.core.exceptions import ValidationError
from django.http import FileResponse
from django.core.files import File
from .Send import Email
from .planilha import export_to_excel

import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from django.http import HttpResponse
import pandas as pd
from openpyxl.styles import PatternFill
from .models import Unidade, Laboratorio, Equipamento, RegimentoInterno  # Adicione outros modelos conforme necessário


def visualizar_pdf(request, unidade_academica_id):
    try:
        unidade_academica = UnidadeAcademica.objects.get(id=unidade_academica_id)
        
        if unidade_academica and unidade_academica.pdf:
            pdf_file = unidade_academica.pdf
            response = FileResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{pdf_file.name}"'
            return response
    except UnidadeAcademica.DoesNotExist:
        pass

    return HttpResponse("PDF não encontradoooo.", status=404)

def visualizar_regimento_interno(request, regimento_id):
    try:
        regimento = RegimentoInterno.objects.get(id=regimento_id)

        if regimento and regimento.pdf:
            pdf_file = regimento.pdf
            response = FileResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{pdf_file.name}"'
            return response
    except RegimentoInterno.DoesNotExist:
        pass

    return HttpResponse("Regimento Interno não encontrado.", status=404)

def editar_regimentos_internos(request, laboratorio_id):
    laboratorio = get_object_or_404(Laboratorio, id=laboratorio_id)
    regimentos_internos = RegimentoInterno.objects.filter(laboratorio=laboratorio)

    if request.method == 'POST':
        regimento_pdf = request.FILES.get('regimento_pdf')
        
        if regimento_pdf:
            regimento_interno = RegimentoInterno(
                laboratorio=laboratorio,
                pdf=regimento_pdf
            )
            regimento_interno.save()
            return redirect('editar_regimentos_internos', laboratorio_id=laboratorio_id)

    return render(request, 'editar_regimentos_internos.html', {
        'laboratorio': laboratorio,
        'regimentos_internos': regimentos_internos,
    })

def editar_unidades_academicas(request, laboratorio_id):
    laboratorio = get_object_or_404(Laboratorio, id=laboratorio_id)
    unidades_academicas = UnidadeAcademica.objects.filter(laboratorio=laboratorio)

    if request.method == 'POST':
        # Lógica para processar o envio da Unidade Acadêmica aqui, se necessário
        unidade_academica_pdf = request.FILES.get('unidade_academica_pdf')
        if unidade_academica_pdf:
            UnidadeAcademica.objects.create(laboratorio=laboratorio, pdf=unidade_academica_pdf)

    return render(request, 'editar_unidades_academicas.html', {
        'laboratorio': laboratorio,
        'unidades_academicas': unidades_academicas,
    })


def visualizar_laboratorio(request, laboratorio_id):
    laboratorio = get_object_or_404(Laboratorio, id=laboratorio_id)

    # Recupere todas as infraestruturas associadas a este laboratório
    infraestruturas = LaboratorioInfraestrutura.objects.filter(laboratorio=laboratorio)

    return render(request, 'view.html', {'laboratorio': laboratorio, 'infraestruturas': infraestruturas})


def index(request):
    return render(request, 'index.html')

# @login_required
def edit(request):
   
    laboratorios = Laboratorio.objects.all()
    marcas = Marca.objects.all()
    equipamentos = Equipamento.objects.all()

    return render(request, 'edit.html', {
        'laboratorios': laboratorios,
        'marcas': marcas,
        'equipamentos': equipamentos,
    })

def imagem_rgb(request, imagem_id):
    try:
        imagem = ImagemLaboratorio.objects.get(pk=imagem_id)
        imagem_bin = imagem.imagem

        response = HttpResponse(content_type="image/jpeg")
        image = Image.open(io.BytesIO(imagem_bin))
        
        # Redimensionar a imagem para o tamanho desejado (600x900)
        # new_size = (600, 900)
        # image = image.resize(new_size, Image.ANTIALIAS)
        
        image = image.convert("RGB")
        image.save(response, format="JPEG")

        return response
    except ImagemLaboratorio.DoesNotExist:
        return HttpResponse("Imagem não encontrada.", status=404)

    
    
from django.db.models import Max

def main(request):
    laboratorios = Laboratorio.objects.annotate(max_imagem=Max('imagens__data_upload')).all()

    lab = Laboratorio.objects.all()

    context = {
        'lab': lab,
        'laboratorios': laboratorios,
    }

    print("DEBUG: Laboratórios:", laboratorios)

    return render(request, 'main.html', context)

def salvar_laboratorio(request):
    if request.method == "POST":
        try:
            imagens_lab = request.FILES.getlist("imagens_lab[]")
            imagens_salvas = []

            for imagem in imagens_lab:
                imagem_laboratorio = ImagemLaboratorio(imagem=imagem)
                imagem_laboratorio.save()
                imagens_salvas.append(imagem_laboratorio)
            
            # if not imagens_lab:
            #         # Caminho para a imagem padrão (ajuste o caminho conforme necessário)
            #     caminho_imagem_padrao = '/uea-news/templates/static/images/generica.png'
                    
            #     with open(caminho_imagem_padrao, 'rb') as img_padrao:
            #             # Crie uma instância de ImagemLaboratorio com a imagem padrão
            #          imagem_laboratorio = ImagemLaboratorio(imagem=File(img_padrao))
            #          imagem_laboratorio.save()
                        
            #             # Adicione a imagem padrão à lista de imagens
            #          imagens_salvas.append(imagem_laboratorio)

            nome_laboratorio = request.POST.get("nome_laboratorio")
            responsavel = request.POST.get("responsavel")
            email = request.POST.get("email")
            telefone = request.POST.get("telefone")
            unidade = request.POST.get("unidade")
            rua = request.POST.get("rua")
            numero_rua = request.POST.get("numero_rua")
            cep = request.POST.get("cep")
            bairro = request.POST.get("bairro")
           
            ato_anexo = request.FILES.get("ato_anexo")
            ato_anexo_content = ato_anexo.read() if ato_anexo else None
            apresentacao = request.POST.get("apresentacao")
            objetivos = request.POST.get("objetivos")

            apresentacao = apresentacao if apresentacao else None
            objetivos = objetivos if objetivos else None
            
            descricao = request.POST.get("descricao")
            link_pnipe = request.POST.get("link_pnipe")

            andar = request.POST.get("andar")
            sala = request.POST.get("sala")

            andar = andar if andar else None
            sala = sala if sala else None


            unidade = unidade if unidade else None
            bairro =  bairro if bairro else None
            rua = rua if rua else None
            numero_rua = numero_rua if numero_rua else None
            cep = cep if cep else None
            apresentacao = apresentacao if apresentacao else None
            objetivos = objetivos if objetivos else None
            descricao = descricao if descricao else None
            link_pnipe = link_pnipe if link_pnipe else None


            equipamento_id = request.POST.get('equipamento')  # Troquei 'equipamento_id' por 'equipamento'
            marca_id = request.POST.get('marca')  # Troquei 'marca_id' por 'marca'
            modelo = request.POST.get('modelo')
            finalidade = request.POST.get('finalidade')

            # Email(email, nome_laboratorio, responsavel)
            # export_to_excel(request=request)
            try:
                equipamento = Equipamento.objects.get(id=equipamento_id)
            except Equipamento.DoesNotExist:
                equipamento = None
            try:
                marca = Marca.objects.get(id=marca_id)
            except Marca.DoesNotExist:
                marca = None

            equipamento = equipamento if equipamento else None
            marca = marca if marca else None
            modelo = modelo if modelo else None
            finalidade = finalidade if finalidade else None

            # Salvar os dados no banco de dados
            laboratorio = Laboratorio.objects.create(
                nome_laboratorio=nome_laboratorio,
                responsavel=responsavel,
                email=email,
                telefone=telefone,
                unidade=unidade,
                rua=rua,
                ato_anexo=ato_anexo_content,
                numero_rua=numero_rua,
                cep=cep,
                bairro=bairro,
                
                apresentacao=apresentacao,
                objetivos=objetivos,
                descricao=descricao,
                link_pnipe=link_pnipe,
            )
            pdf_unidade_academica = request.FILES.get("pdf_unidade_academica")
            if pdf_unidade_academica:
                # Certifique-se de que o arquivo seja um PDF (você pode adicionar validações adicionais)
                if not pdf_unidade_academica.name.endswith('.pdf'):
                    raise ValidationError("O arquivo deve ser um PDF.")
                
                # Crie uma instância de UnidadeAcademica e associe-a ao laboratório
                unidade_academica = UnidadeAcademica(laboratorio=laboratorio, pdf=pdf_unidade_academica)
                unidade_academica.save()
         # Salvar as imagens no banco de dados (caso você tenha um modelo separado para imagens)
            infraestrutura = Infraestrutura.objects.create(
            equipamento=equipamento,
            marca=marca,
            modelo=modelo,
            finalidade=finalidade,
            )
            
            laboratorio.infraestrutura = infraestrutura
            laboratorio.save()

            
            # Relacionar as imagens ao laboratório
            laboratorio.imagens.set(imagens_salvas)

            if imagens_salvas:
                return HttpResponseRedirect(reverse('editar_laboratorio', args=[laboratorio.id, imagens_salvas[0].id]))
            else:
                # Lida com o caso em que não há imagens salvas
                caminho_imagem_padrao = static('images/download.jpeg')  # Ajuste o caminho aqui
                messages.add_message(request, messages.WARNING, 'Nenhuma imagem foi salva.')

                return HttpResponseRedirect(reverse('editar_laboratorio', args=[laboratorio.id, 0]))  # Defina 0 como o ID da imagem padrão

        except Exception as e:
            print('Erro:', str(e))
            print('Erro ao salvar')
            messages.add_message(request, messages.WARNING, 'O sistema apresenta falhas internas.')
            return redirect('../edit/')
    else:
        return render(request, 'edit.html')
    
def adicionar_grupo_de_pesquisa(request, laboratorio_id=None):
    laboratorio = get_object_or_404(Laboratorio, id=laboratorio_id) if laboratorio_id else request.user.laboratorio

    if request.method == 'POST':
        nome_do_grupo = request.POST.get('nome_do_grupo')
        area = request.POST.get('area')
        link_grupo = request.POST.get('link_grupo')

        # Crie uma nova instância de GrupoDePesquisa com os dados fornecidos
        grupo_de_pesquisa = GrupoDePesquisa.objects.create(
            nome_do_grupo=nome_do_grupo,
            area=area,
            link_grupo=link_grupo
        )

        # Associe o grupo de pesquisa ao laboratório atual
        laboratorio.grupos_de_pesquisa.add(grupo_de_pesquisa)

        # Redirecione para a página de edição do laboratório ou para onde for adequado
        return redirect('editar_laboratorio', laboratorio.id, 0)

    grupos_de_pesquisa = laboratorio.grupos_de_pesquisa.all()

    return render(
        request,
        'adicionar_grupo_de_pesquisa.html',
        {'laboratorio': laboratorio, 'grupos_de_pesquisa': grupos_de_pesquisa}
    )
    
def editar_infraestrutura(request, laboratorio_id):
    laboratorio = get_object_or_404(Laboratorio, id=laboratorio_id)
    marcas = Marca.objects.all()
    equipamentos = Equipamento.objects.all()
    infraestruturas = laboratorio.infraestruturas.all()

    if request.method == 'POST' and 'salvar_infraestrutura' in request.POST:
        equipamento_id = request.POST.get('equipamento')
        marca_id = request.POST.get('marca')
        modelo = request.POST.get('modelo')
        finalidade = request.POST.get('finalidade')

        # Verifique se uma imagem foi enviada
        novas_imagens = request.FILES.getlist('nova_imagem')

        # Crie uma nova infraestrutura
        infraestrutura = Infraestrutura.objects.create(
            equipamento_id=equipamento_id,
            marca_id=marca_id,
            modelo=modelo,
            finalidade=finalidade,
        )

        # Associe a nova infraestrutura ao laboratório atual
        LaboratorioInfraestrutura.objects.create(laboratorio=laboratorio, infraestrutura=infraestrutura)

        # Se uma nova imagem foi enviada, crie uma instância de ImagemInfraestrutura para cada imagem
        for nova_imagem in novas_imagens:
            imagem_infraestrutura = ImagemInfraestrutura(imagem=nova_imagem, infraestrutura=infraestrutura)
            imagem_infraestrutura.save()

        print('Infraestrutura criada com sucesso!')
        # Redirecione para a página de edição do laboratório ou para onde for adequado
        return HttpResponseRedirect(reverse('editar_laboratorio', args=[laboratorio.id, 0]))

    return render(
        request,
        'editar_infraestrutura.html',
        {'laboratorio': laboratorio, 'marcas': marcas, 'equipamentos': equipamentos, 'infraestruturas': infraestruturas}
    )

def equipamento(request):
   
    laboratorios = Laboratorio.objects.all()
  
    return render(request, 'equipamento.html', {
        'laboratorios': laboratorios,
    })

def salvar_equipamento(request):
    if request.method == "POST":
        try:   
            equipamento = request.POST.get("equipamento")
            marca = request.POST.get("marca")
            modelo = request.POST.get("modelo")
            finalidade = request.POST.get("finalidade")
          

  # Salvar os dados no banco de dados
            Infraestrutura.objects.create(
                equipamento=equipamento,
                marca=marca,
                modelo=modelo,
                finalidade=finalidade,
                
            )

            messages.add_message(request, messages.SUCCESS, 'Salvo com sucesso.')
            return render(request, 'equipamento.html')
        except:
            messages.add_message(request, messages.WARNING, 'O sistema apresenta falhas internas.')
            return redirect('../equipamento/')
    else:
        return render(request, 'equipamento.html')



def paginar(list, limit_per_page, request): 
    paginator = Paginator(list, limit_per_page) 
    page = request.GET.get('page')
    atos = paginator.get_page(page)
    context = {'atos': atos}
    return context

@login_required
def aprovados(request):
    atos_list = AtoNormativ.objects.filter(status='aprovado')
    context = paginar(atos_list, 16, request);
    return render(request, 'main.html', context)


def pesquisar(request):
    if request.method == 'GET':
        termo_pesquisa = request.GET.get('pesquisa', '')  # Obtém o termo de pesquisa do parâmetro GET 'pesquisa'
        atos = AtoNormativ.objects.filter(texto_normativo__icontains=termo_pesquisa)  # Filtra os atos com base no termo de pesquisa
        context = {'atos': atos}
        return render(request, 'resultado_pesquisa.html', context)
    
def visualizar_arquivo(request, laboratorio_id):
    try:
        laboratorio = Laboratorio.objects.get(pk=laboratorio_id)
        if laboratorio.ato_anexo:
            response = HttpResponse(laboratorio.ato_anexo, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="arquivo.pdf"'  # Pode ajustar o nome do arquivo
            return response
    except Laboratorio.DoesNotExist:
        pass

    return HttpResponse("Arquivo não encontrado.", status=404)

def visualizar_imagens(request, laboratorio_id):
    laboratorio = Laboratorio.objects.get(pk=laboratorio_id)
    imagens = laboratorio.imagens.all()
    return render(request, 'visualizar_imagens.html', {'laboratorio': laboratorio, 'imagens': imagens})

def view_imagem(request, imagem_id):
    try:
        imagem = ImagemLaboratorio.objects.get(pk=imagem_id)
        imagem_bin = imagem.imagem

        # Configurar o cabeçalho de tipo de conteúdo para uma imagem
        response = HttpResponse(content_type="image/jpeg")
        
        # Abra a imagem usando o Pillow (PIL)
        image = Image.open(io.BytesIO(imagem_bin))

        # Converta a imagem para o modo RGB
        image = image.convert("RGB")
        
        # Salve a imagem no formato JPEG
        image.save(response, format="JPEG")

        return response
    except ObjectDoesNotExist:
        return HttpResponse("Imagem não encontrada.", status=404)

def editar_laboratorio(request, laboratorio_id, imagem_id):
    laboratorio = get_object_or_404(Laboratorio, id=laboratorio_id)

    if request.method == 'POST':
        # Processar os campos do formulário
        laboratorio.nome_laboratorio = request.POST.get('nome_laboratorio', '')
        laboratorio.responsavel = request.POST.get('responsavel', '')
        laboratorio.email = request.POST.get('email', '')
        laboratorio.data_criacao = request.POST.get('data_criacao', '')
        laboratorio.apresentacao = request.POST.get('apresentacao', '')
        laboratorio.objetivos = request.POST.get('objetivos', '')
        laboratorio.descricao = request.POST.get('descricao', '')
        laboratorio.link_pnipe = request.POST.get('link_pnipe', '')

        # Outros campos...

        # Processar a imagem, se presente
        imagem_laboratorio = request.FILES.get('imagem_laboratorio')
        if imagem_laboratorio:
            # Crie uma instância de ImagemLaboratorio associada ao laboratório
            imagem = ImagemLaboratorio(imagem=imagem_laboratorio)
            imagem.save()
            laboratorio.imagens.add(imagem)

        laboratorio.save()
        messages.success(request, 'Laboratório atualizado com sucesso.')
        return redirect('editar_laboratorio', laboratorio_id=laboratorio.id, imagem_id=imagem_id)

    # Inclua o objeto laboratorio no contexto
    return render(request, 'editar_laboratorio.html', {'laboratorio': laboratorio})

def editar_endereco(request, laboratorio_id):
    laboratorio = get_object_or_404(Laboratorio, pk=laboratorio_id)

    if request.method == 'POST':
        try:
            # Recupere os valores atualizados dos campos de endereço do formulário
            unidade = request.POST.get('unidade')
            rua = request.POST.get('rua')
            numero_rua = request.POST.get('numero_rua')
            cep = request.POST.get('cep')
            bairro = request.POST.get('bairro')
            andar = request.POST.get('andar')
            sala = request.POST.get('sala')

            # Atualize os campos de endereço do objeto Laboratorio
            laboratorio.unidade = unidade
            laboratorio.rua = rua
            laboratorio.numero_rua = numero_rua
            laboratorio.cep = cep
            laboratorio.bairro = bairro
            laboratorio.andar=andar
            laboratorio.sala=sala

            # Salve o objeto Laboratorio atualizado no banco de dados
            laboratorio.save()

            # Adicione uma mensagem de sucesso
            messages.success(request, 'Endereço atualizado com sucesso.')

            # Redirecione para a página de detalhes do laboratório ou para onde desejar
            # Neste exemplo, estamos redirecionando para a página de edição de endereço novamente
            return redirect('editar_endereco', laboratorio_id=laboratorio_id)
        except Exception as e:
            # Trate qualquer exceção que possa ocorrer
            print('Erro:', str(e))
            messages.error(request, f'Erro ao atualizar o endereço: {str(e)}')

    # Renderize o template com os detalhes do laboratório e o formulário para edição de endereço
    return render(request, 'editar_endereco.html', {'laboratorio': laboratorio})


def visualizar_membros_laboratorio(request, laboratorio_id):
    laboratorio = get_object_or_404(Laboratorio, id=laboratorio_id)
    membros = laboratorio.membros.all()

    if request.method == 'POST':
        # Lógica para adicionar ou atualizar membros, se necessário
        nome_membro = request.POST.get('nome_membro')
        funcao = request.POST.get('funcao')
        curriculo_lattes = request.POST.get('curriculo_lattes')

        if nome_membro and funcao:
            membro, created = MembroLaboratorio.objects.get_or_create(
                laboratorio=laboratorio,
                nome_membro=nome_membro,
                defaults={'funcao': funcao, 'curriculo_lattes': curriculo_lattes}
            )

    return render(
        request,
        'visualizar_membros.html',
        {'laboratorio': laboratorio, 'membros': membros}
    )


def export_to_excel(request):

    if request.method == "POST":
        unidade = request.POST.get('unidade')
        export_all = request.POST.get('export_all')


        if unidade:
            laboratorios = Laboratorio.objects.filter(unidade=unidade)
            equipamentos = Infraestrutura.objects.all()
            regimentos_internos = RegimentoInterno.objects.all()

        if export_all:
            laboratorios = Laboratorio.objects.all()
            equipamentos = Infraestrutura.objects.all()
            regimentos_internos = RegimentoInterno.objects.all()

    print(laboratorios)

    # usuario = Unidade.objects.all()
    # print(usuario)

    laboratorios_df = pd.DataFrame(list(laboratorios.values()))
    regimentos_internos_df = pd.DataFrame(list(regimentos_internos.values()))
    equipamentos_df = pd.DataFrame(list(equipamentos.values()))

    # Verifique se 'laboratorio_id' existe em equipamentos_df
    if 'laboratorio_id' in equipamentos_df.columns:
        equipamentos_df = equipamentos_df.drop(columns=['laboratorio_id'])

    # Combine os DataFrames
    combined_df = pd.merge(laboratorios_df, regimentos_internos_df, left_on='id', right_on='laboratorio_id', how='left')
    combined_df = pd.merge(combined_df, equipamentos_df, left_on='laboratorio_id', right_on='id', how='left')

    # Reorganize pelo ID (ou outro campo desejado)
    combined_df = combined_df.sort_values(by='id')

    # Remova as colunas 'id' e 'laboratorio_id'
    combined_df = combined_df.drop(columns=['id', 'laboratorio_id', 'id_x', 'id_y'])

    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    worksheet.title = 'Laboratório'

    fill_green_dark = PatternFill(start_color="008000", end_color="008000", fill_type="solid")

    row_colors = ['00ff00', '4aea37', '70bf5d', '79aa6b', '7e9576', '808080']

    for col_idx, column_name in enumerate(combined_df.columns, 1):
        cell = worksheet.cell(row=1, column=col_idx, value=column_name)
        cell.fill = fill_green_dark

    for row_idx, row in enumerate(combined_df.itertuples(), 2):
        row_color = row_colors[row_idx % len(row_colors)]
        for col_idx, value in enumerate(row[1:], 1):
            cell = worksheet.cell(row=row_idx, column=col_idx, value=value)
            cell.fill = PatternFill(start_color=row_color, end_color=row_color, fill_type="solid")

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="laboratorios_data.xlsx"'

    workbook.save(response)

    return response
    




