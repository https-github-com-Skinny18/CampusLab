from django.shortcuts import render, get_object_or_404, redirect
from django.utils.html import strip_tags
from django.contrib import messages
from django.contrib.messages import constants
from io import BytesIO
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4 
from django.contrib import messages
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.views.generic.edit import UpdateView
from core.models import AtoNormativ
from django.core.paginator import Paginator
from django.views import View
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import letter
from .models import AtoNormativ, Autoridade
from django.contrib.auth import logout

def index(request):
    return render(request, 'index.html')

def view(request, ato_id):
    ato = get_object_or_404(AtoNormativ, pk=ato_id)
    context = {'ato': ato}
    return render(request, 'view.html', context)

# def authetication(request):
#     return render(request, 'authentication.html')

@login_required
def edit(request):
    # View para exibir a página de edição
    
    # composicoes = Composicao.objects.all()
    atonormativs = AtoNormativ.objects.all()
    autoridades = Autoridade.objects.all()
    
    # tipo_atos = Composicao.objects.values_list('tipo_ato', flat=True).distinct()
    
    return render(request, 'edit.html', {
        # 'composicoes' : composicoes,
        'atonormativs': atonormativs,
        'autoridades' : autoridades,
        # 'tipo_atos': tipo_atos,
    })


def salvar_ato(request):

    if request.method != "POST":
        return render(request, 'edit.html')

    elif request.method == "POST":
        textoNormativo = request.POST.get("textoNormativo")
        textoEmenta = request.POST.get("textoEmenta")
        nomeAutoridadeAssinantePrimaria = request.POST.get("nomeAutoridadeAssinantePrimaria")
        nomeAutoridadeAssinanteSecundaria = request.POST.get("nomeAutoridadeAssinanteSecundaria")
        tipoAto = request.POST.get("tipoAto")
        anoDePublicacao = request.POST.get("anoDePublicacao")
        numeroAto = request.POST.get("numeroAto")
        paginaDOE = request.POST.get("paginaDOE")
        secaoDOE = request.POST.get("secaoDOE")
        numeroDOE = request.POST.get("numeroDOE")
        cargoDaAutoridadePrimaria = request.POST.get("cargoDaAutoridadePrimaria")
        cargoDaAutoridadeSecundaria = request.POST.get("cargoDaAutoridadeSecundaria")

    try:
        nomeAutoridadeAssinantePrimaria = Autoridade.objects.get(id=nomeAutoridadeAssinantePrimaria)
        nomeAutoridadeAssinanteSecundaria = Autoridade.objects.get(id=nomeAutoridadeAssinanteSecundaria)

        # Salvar os dados no banco de dados
        AtoNormativ.objects.create(
            texto_normativo=textoNormativo,
            ementa=textoEmenta,
            ano=anoDePublicacao,
            numero=numeroAto,
            doe_pagina=paginaDOE,
            doe_secao=secaoDOE,
            doe_numero=numeroDOE,
            assinante1=nomeAutoridadeAssinantePrimaria,
            assinante2=nomeAutoridadeAssinanteSecundaria,
            autoridade1=cargoDaAutoridadePrimaria,
            autoridade2=cargoDaAutoridadeSecundaria,
            tipo_ato=tipoAto,
            status='revisao',
        )
        
        messages.add_message(request, constants.SUCCESS, 'Salvo com sucesso.')
        return render(request, 'edit.html')
    
    except:
        messages.add_message(request, constants.WARNING, 'O sistema apresenta falhas internas.')
        return redirect('../edit/')

def mm2p(milimetros):
    return milimetros / 0.352777

def mm2p(mm_value):
    return mm_value * 2.83465

class GerarPDFView(View):
    def get(self, request, ato_id):
        # Recupera o objeto Ato correspondente ao ID fornecido
        ato = get_object_or_404(AtoNormativ, id=ato_id)

        # Cria o objeto HttpResponse com o tipo MIME apropriado para PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{ato.autoridade1}.pdf"'
        # response['Content-Disposition'] = f'inline; filename="{ato.ementa}.pdf"'


        # Cria o objeto PDF com o objeto HttpResponse
        pdf = canvas.Canvas(response, pagesize=letter)

        # Adiciona o texto do tipo do ato ao PDF
        try:
            pdf.drawString(10, 10, ato.tipo_ato)
        except AttributeError:
            pdf.drawString(10, 10, "Tipo do ato não disponível")

        # Adiciona a imagem ao topo da página
        logo_path = '/home/lury/Área de Trabalho/projeto/uea-news/templates/static/images/logo-governo.jpg'
        logo_width = 270  # largura desejada da imagem
        logo_height = 115  # altura desejada da imagem

        # Calcula a posição X (horizontal) para centralizar a imagem
        logo_x = (letter[0] - logo_width) / 2

        # Calcula a posição Y (vertical) para centralizar a imagem
        logo_y = letter[1] - 100

        # Desenha a imagem com o tamanho e posição desejados
        pdf.drawImage(logo_path, logo_x, logo_y, width=logo_width, height=logo_height)

        linha_comprimento = 550  # define o comprimento da linha
        linha_y = logo_y - (-20)  # define a posição vertical da linha

        # Desenha a linha logo abaixo da imagem
        pdf.line((letter[0] - linha_comprimento) / 2, linha_y, (letter[0] + linha_comprimento) / 2, linha_y)

        # Define a altura do footer
        footer_height = 12

        # Desenha a linha como footer
        footer_y = footer_height

        # Define o novo texto a ser adicionado
        text = "Governo do Estado do Amazonas"

        # Define a fonte e o tamanho do texto
        font_name = "Helvetica-Bold"
        font_size = 10
        font_name2 = "Helvetica"
        font_size2 = 8

        # Define a posição X (horizontal) para centralizar o texto
        text_x = (letter[0] - pdf.stringWidth(text, font_name, font_size)) / 2

        # Define a posição Y (vertical) do texto
        text_y = footer_y + 20

        # Adiciona o novo texto ao PDF
        pdf.setFont(font_name, font_size)
        pdf.drawString(text_x, text_y, text)

        # Define o segundo texto a ser adicionado
        text2 = "Av. Brasil, 3925 - Compensa II - Manaus-AM - CEP 69036-110"

        # Define a posição X (horizontal) para centralizar o texto
        text2_x = (letter[0] - pdf.stringWidth(text2, font_name, font_size)) / 2

        # Define a posição Y (vertical) do segundo texto
        text2_y = text_y - font_size - 8

        # Adiciona o segundo texto ao PDF
        pdf.setFont(font_name2, font_size)
        pdf.drawString(text2_x, text2_y, text2)

        # Define a posição X (horizontal) e Y (vertical) da assinatura
        ass_x = 20
        ass_y = logo_y - 350

        # Define o texto a ser adicionado abaixo da assinatura
        ass_text = "Assinado por: ANDRÉ LUIZ NUNES ZOGAHIB"
        ass_text2 = "Data: 10/05/2023"

        # Adiciona a assinatura
        pdf.setFont(font_name2, font_size2)
        pdf.drawString(ass_x, ass_y, ass_text)

        # Define o texto a ser adicionado abaixo da assinatura
        data_text = "Data: 10/05/2023 14:00 AM -04:00"

        # Define a posição X (horizontal) da data
        data_x = ass_x

        # Define a posição Y (vertical) da data
        data_y = ass_y - 10

        # Adiciona o texto da data ao PDF
        pdf.setFont(font_name2, font_size2)
        pdf.drawString(data_x, data_y, data_text)

        # Desenha a linha de rodapé
        pdf.line((letter[0] - linha_comprimento) / 2, footer_y - (-35), (letter[0] + linha_comprimento) / 2, footer_y - (-35))

        # Ajusta a altura do footer para incluir os textos
        footer_y = text2_y - font_size - 40

        # Quando acabamos de inserir 'coisas no PDF'
        pdf.showPage()
        pdf.save()

        # Retorna o HttpResponse contendo o PDF gerado
        return response
    
# def gerar_pdf(request, ato_id):
#     # Recupera o objeto Ato correspondente ao ID fornecido
#     ato = AtoNormativ.objects.get(id=ato_id)

#     # Cria o objeto HttpResponse com o tipo MIME apropriado para PDF
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="{ato.autoridade1}.pdf"'

#     # Cria o objeto PDF com o objeto HttpResponse
#     pdf = canvas.Canvas(response)

#     # Adiciona o texto do tipo do ato ao PDF
#     try:
#         pdf.drawString(mm, mm*265, ato.tipo_ato)
#     except AttributeError:
#         pdf.drawString(mm, mm*265, "Tipo do ato não disponível")

#     # Adiciona outros elementos ao PDF...

#     # Fecha o objeto PDF e retorna o HttpResponse
#     pdf.showPage()
#     pdf.save()
#     return response
        

def editar_ato(request, ato_id):
    ato = get_object_or_404(AtoNormativ, pk=ato_id)

    if request.method == 'POST':
        ato.texto_normativo = request.POST.get('texto_normativo')
        ato.ementa = request.POST.get('ementa')
        ato.ano = request.POST.get('ano')
        ato.numero = request.POST.get('numero')
        ato.doe_pagina = request.POST.get('doe_pagina')
        ato.doe_secao = request.POST.get('doe_secao')
        ato.doe_numero = request.POST.get('doe_numero')
        autoridade1_id = request.POST.get('cargoDaAutoridadePrimaria')
        ato.autoridade1 = Autoridade.objects.get(pk=autoridade1_id).nome if autoridade1_id else None
        ato.autoridade2 = request.POST.get('cargoDaAutoridadeSecundaria')
        assinante1_id = request.POST.get('assinante1')
        ato.assinante1 = Autoridade.objects.get(pk=assinante1_id) if assinante1_id else None
        ato.tipo_ato = request.POST.get('tipo_ato')
        ato.status = request.POST.get('status')
        ato.save()
        messages.success(request, 'Ato atualizado com sucesso.')
        return redirect('view', ato_id=ato.id)

    autoridades = Autoridade.objects.all()
    if request.POST.get('aprovar_ato'):
        ato.status = 'aprovado'
        ato.save()
        return redirect('main')
    
    context = {'ato': ato, 'autoridades': autoridades}
    return render(request, 'editar_ato.html', context)

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

@login_required
def cancelados(request):
    atos_list = AtoNormativ.objects.filter(status='cancelado')
    context = paginar(atos_list, 16, request);
    return render(request, 'main.html', context)

@login_required
def rascunhos(request):
    atos_list = AtoNormativ.objects.filter(status='rascunho')
    context = paginar(atos_list, 16, request);
    return render(request, 'main.html', context)

@login_required
def revisao(request):
    atos_list = AtoNormativ.objects.filter(status='revisao')
    context = paginar(atos_list, 16, request);
    return render(request, 'main.html', context)

@login_required
def pendentes(request):
    atos_list = AtoNormativ.objects.filter(status='pendente')
    context = paginar(atos_list, 16, request);
    return render(request, 'main.html', context)
