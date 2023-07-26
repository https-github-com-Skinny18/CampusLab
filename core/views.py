from django.shortcuts import render, get_object_or_404, redirect
from .models import  AtoNormativ, Autoridade
from django.utils.html import strip_tags
from django.contrib import messages
from django.contrib.messages import constants
from io import BytesIO
from reportlab.pdfgen import canvas
from django.contrib import messages
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from core.models import AtoNormativ
from django.core.paginator import Paginator
from django.views import View
from reportlab.lib.pagesizes import letter
from datetime import datetime
from reportlab.lib import colors
from core.Portaria import Portaria
from core.Boletim import Boletim
from django.db.models import Q
from .models import BoletimGerado


def index(request):
    return render(request, 'index.html')
    
def view(request, ato_id):
    ato = get_object_or_404(AtoNormativ, pk=ato_id)
    context = {'ato': ato}
    return render(request, 'view.html', context)

def authetication(request):
    return render(request, 'authentication.html')

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

def salvar_boletim(request, ato_ids):
        
        ato_ids_list = [int(id) for id in ato_ids.split(',')]

        
            # Criar o boletim combinando os atos selecionados
        atos_selecionados = []
        for ato_id in ato_ids_list:
            ato = get_object_or_404(AtoNormativ, id=ato_id)
            atos_selecionados.append(ato)
        ids_serializados = ','.join(str(id) for id in ato_ids_list)
        print(ids_serializados)
        # Salvar o PDF gerado no banco de dados
        boletim = BoletimGerado.objects.create(
            portarias_fks=ids_serializados,
            titulo=f"Boletim - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            conteudo_pdf=atos_selecionados,
        )
        {"boletim_id": boletim.id}
        print(boletim.id)
        messages.add_message(request, constants.SUCCESS, 'Boletim salvo com sucesso.')
        return redirect('boletins_salvos')




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
        textoNormativoSantinizado = strip_tags(textoNormativo)
        textoEmentaSanitizado = strip_tags(textoEmenta)

        try:
            nomeAutoridadeAssinantePrimaria = Autoridade.objects.get(id=nomeAutoridadeAssinantePrimaria)
            nomeAutoridadeAssinanteSecundaria = Autoridade.objects.get(id=nomeAutoridadeAssinanteSecundaria)

            # Salvar os dados no banco de dados
            AtoNormativ.objects.create(
                texto_normativo=textoNormativoSantinizado,
                ementa=textoEmentaSanitizado,
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

    def get(self, request, ato_ids, boletim_id):

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="documento.pdf"'
        packet = BytesIO()
         
        if isinstance(ato_ids, str) and ',' in ato_ids:
            
            boletim = Boletim()         
            pdf = canvas.Canvas(packet)
            ato_ids_list = [int(id) for id in ato_ids.split(',')]
            atos = []
            for i in ato_ids_list:
                atos.append(get_object_or_404(AtoNormativ, id=i))
            boletins = get_object_or_404(BoletimGerado, id=boletim_id)
            print(boletins.id)
            boletim_path = '/home/gabriel/Documentos/uea-news/templates/static/images/boletim.jpg'
            CAPA_TITULO = "BOLETIM N°" + str(boletins.id)

            boletim.desenharCapa(pdf, boletim_path, CAPA_TITULO)

            def add_page():
                pdf.showPage()
                boletim.draw_header(pdf)

            conta_cata_subtitulo = 'UNIVERSIDADE DO ESTADO DO AMAZONAS'
            doe = CAPA_TITULO
            boletim.desenharContraCapa(pdf, doe, conta_cata_subtitulo)

            pdf.setFont('Helvetica-Bold', 12)
            
            assinante_unicas = []
            autoridade = ""
            asdf = 620
            y = 600
            for ato in atos:
                assinante_atual = str(ato.assinante1).split('/')[0]
                assinante2 = str(ato.assinante2)
                autoridade = ato.autoridade1
                autoridade2 = ato.autoridade2
                print(autoridade2)
                if assinante_atual and assinante_atual not in assinante_unicas:
                    assinante_unicas.append(assinante_atual)
                    pdf.setFont('Helvetica', 12)
                    pdf.drawString(280, asdf, assinante_atual)
                    pdf.drawString(280, y, assinante2)
                    pdf.setFont('Helvetica-Bold', 12)
                    pdf.drawString(280, 610, autoridade)
                    pdf.drawString(280, 580, autoridade2)

                    y -= 20
                    asdf -= 20


            add_page()

            y = 650 
           
            boletim.desenharSumario(pdf, doe, conta_cata_subtitulo)
            for ato in atos:

                ato_posicao = pdf.stringWidth(ato.tipo_ato, 'Helvetica-Bold', 12)

                data_str = str(ato.doe_data)
                ano = data_str[0:4]

                doe_str = str(ato.numero)
                doe = "PORTARIA N°" + doe_str + "/" + ano
                pdf.setFont('Helvetica-Bold', 12)
                pdf.drawString(180, y, doe)
                pdf.setFont("Helvetica", 12)
                y -= 20 
            add_page()

            
            
            x = 70
            y = 650
            tamanho_fonte = 12
            limite_largura = 520
            limite_altura = 100
            espacamento_margem = 10  # Espaçamento desejado para as margens

        
            for ato in atos:
                assinatura = str(ato.assinante1).split('/')[0]
                assinatura2 = ato.assinante2

                paragrafos = ato.texto_normativo.splitlines()
                for index, paragrafo in enumerate(paragrafos):
                    if index == 0:
                        pdf.setFont("Helvetica-Bold", 12)
                        pdf.drawString(240, y, ato.tipo_ato.upper())

                        ato_posicao = pdf.stringWidth(ato.tipo_ato, 'Helvetica-Bold', 12)
                        n_posicao = 304 + ato_posicao + -43
                        limite_x = 550  # Limite horizontal do documento
                        if n_posicao > limite_x:
                            n_posicao = limite_x

                        data_str = str(ato.doe_data)
                        ano = data_str[0:4]

                        doe_str = str(ato.numero)
                        doe = "N°" + doe_str + "/" + ano

                        pdf.setFont('Helvetica-Bold', 12)
                        pdf.drawString(n_posicao, y, doe)
                        pdf.setFont("Helvetica", 12)

                        y -= tamanho_fonte + 2

                    if y - tamanho_fonte < limite_altura:
                        add_page()
                        y = 650

                    # Calcular a largura disponível considerando a margem esquerda e a margem direita
                    largura_disponivel = limite_largura - x

                    if pdf.stringWidth(paragrafo, 'Helvetica', 12) > largura_disponivel:
                        # Verificar se o parágrafo completo cabe na página atual
                        palavras = paragrafo.split(' ')
                        paragrafo_temp = ''
                        for palavra in palavras:
                            if pdf.stringWidth(paragrafo_temp + palavra, 'Helvetica', 12) < largura_disponivel:
                                paragrafo_temp += palavra + ' '
                            else:
                                # Desenhar o parágrafo atual
                                pdf.drawString(x, y, paragrafo_temp)
                                # Atualizar a posição vertical para o próximo parágrafo
                                y -= tamanho_fonte + 2
                                paragrafo_temp = palavra + ' '

                        # Desenhar o restante do parágrafo
                        pdf.drawString(x, y, paragrafo_temp)
                    else:
                        # Desenhar o parágrafo completo
                        pdf.drawString(x, y, paragrafo)

                    if index == len(paragrafos) - 1:
                                # Desenhar a assinatura apenas uma vez no final do parágrafo
                        y_assinatura = y - tamanho_fonte - 1
                        pdf.setFont("Helvetica-Bold", 12)
                        pdf.drawString(200, y_assinatura, assinatura.upper())
                        y = y_assinatura - 15 
                        pdf.setFont('Helvetica', 12)
                        pdf.drawString(180,y, 'UNIVERSIDADE DO ESTADO DO AMAZONAS')
                    y -= tamanho_fonte + 2                    
                    pdf.setFont("Helvetica-Bold", 12)
                    pdf.drawString(250, 750, CAPA_TITULO)
                    data_str = str(ato.doe_data)
                    ano = data_str[0:4]

                    pdf.setFont('Helvetica', 12)
                    pdf.drawString(180, 730, 'UNIVERSIDADE DO ESTADO DO AMAZONAS')
                    pdf.drawString(300,25, f"{pdf.getPageNumber() + 1}")
                y -= espacamento_margem 

        else:

            portaria = Portaria()
            ato = get_object_or_404(AtoNormativ, id=int(ato_ids))
            pdf = canvas.Canvas(response, pagesize=letter)       

            FONT = "Helvetica"
            FONT_BOLD = "Helvetica-Bold"
            font_size2 = 8

            pdf.setFont(FONT_BOLD, 12)

            data_str = str(ato.doe_data)
            ano = data_str[0:4]
            doe = " N°" + str(ato.numero) + "/" + ano

            pdf.drawString(240, 680, ato.tipo_ato.upper() + doe)

            def add_page():
                pdf.showPage()
                portaria.draw_header(pdf)
                portaria.draw_footer(pdf)
            
            limite_largura = 550
            limite_altura = 100

            MARGIN_LEFT = 50
            MARGIN_BOTTOM = 650  
            tamanho_fonte = 12

            portaria.draw_header(pdf)
            portaria.draw_footer(pdf)

            palavras = ato.texto_normativo.split()

            for palavra in palavras:
                largura_palavra = pdf.stringWidth(palavra, FONT, tamanho_fonte)

                if MARGIN_LEFT + largura_palavra < limite_largura:
                    pdf.drawString(MARGIN_LEFT, MARGIN_BOTTOM, palavra )
                    MARGIN_LEFT += largura_palavra + pdf.stringWidth(" ", FONT, tamanho_fonte)
                else:
                    MARGIN_LEFT = 50
                    MARGIN_BOTTOM -= tamanho_fonte + 2

                    if MARGIN_BOTTOM < limite_altura:
                        add_page()
                        MARGIN_BOTTOM = 700

                    pdf.drawString(MARGIN_LEFT, MARGIN_BOTTOM, palavra + " ")
                    MARGIN_LEFT += largura_palavra + pdf.stringWidth("", FONT, tamanho_fonte)

            altura_texto_embaixo = pdf.stringWidth(ato.assinante2, FONT, 12)

            y_embaixo = MARGIN_BOTTOM - tamanho_fonte - altura_texto_embaixo - -20  # Ajuste conforme necessário
            y_abaixo = MARGIN_BOTTOM - tamanho_fonte - altura_texto_embaixo - -9
        
            assinante = ato.assinante2

            pdf.setFont(FONT_BOLD, tamanho_fonte)

            largura_assinante = pdf.stringWidth(assinante, FONT_BOLD, tamanho_fonte)

            y_assinante = y_embaixo + tamanho_fonte

            y_autoridade = y_abaixo + tamanho_fonte

            def centralizar(text):
                return ((letter[0] - text) / 2)

            pdf.drawString(centralizar(largura_assinante), y_assinante, assinante.upper())

            TEXTO_FUNCAO = ato.autoridade1 + " Da Universidade Do Estado Do Amazonas"
            
            largura_autoridade = pdf.stringWidth(TEXTO_FUNCAO, FONT, tamanho_fonte)

            pdf.setFont(FONT, tamanho_fonte)

            pdf.drawString(centralizar(largura_autoridade), y_autoridade, TEXTO_FUNCAO)
            
            DATE_MARGIN_X = 50
            altura_texto_embaixo = pdf.stringWidth(ato.assinante2, FONT, 12)

            y_outro = MARGIN_BOTTOM - tamanho_fonte - altura_texto_embaixo - -10

            data_objeto = datetime.strptime(data_str[:10], "%Y-%m-%d")
            data_br = data_objeto.strftime("%d-%m-%Y")
            
            TEXT_ASSINATURA = "Assinado por: " + ato.assinante2
            TEXT_DATE = f"Data: {data_br}"

            DATA_POSITION_Y = y_outro - 10

            pdf.setFont(FONT, font_size2)

            pdf.drawString(DATE_MARGIN_X, y_outro, TEXT_ASSINATURA)
            pdf.drawString(DATE_MARGIN_X, DATA_POSITION_Y, TEXT_DATE)

        pdf.save()
        response.write(packet.getvalue())
        return response


def editar_ato(request, ato_ids):
    ato = get_object_or_404(AtoNormativ, pk=ato_ids)

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
        print(ato.tipo_ato)
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

def boletim(request):
    atos_list = AtoNormativ.objects.filter(status='revisao')
    context_paginacao = paginar(atos_list, 18, request)


    # Combinando os dois contextos em um único dicionário
    context = {**context_paginacao}

    return render(request, 'boletim.html', context)

def aprovados(request):
    atos_list = AtoNormativ.objects.filter(status='aprovado')
    context = paginar(atos_list, 18, request);
    return render(request, 'main.html', context)

def cancelados(request):
    atos_list = AtoNormativ.objects.filter(status='cancelado')
    context = paginar(atos_list, 18, request);
    return render(request, 'main.html', context)

def rascunhos(request):
    atos_list = AtoNormativ.objects.filter(status='rascunho')
    context = paginar(atos_list, 18, request);
    return render(request, 'main.html', context)

def revisao(request):
    atos_list = AtoNormativ.objects.filter(status='revisao')
    context = paginar(atos_list, 18, request);
    return render(request, 'main.html', context)

def pendentes(request):
    atos_list = AtoNormativ.objects.filter(status='pendente')
    context = paginar(atos_list, 18, request);
    return render(request, 'main.html', context)

def pesquisar(request):
    if request.method == 'GET':
        termo_pesquisa = request.GET.get('pesquisa', '')  # Obtém o termo de pesquisa do parâmetro GET 'pesquisa'
        atos = AtoNormativ.objects.filter(texto_normativo__icontains=termo_pesquisa)  # Filtra os atos com base no termo de pesquisa
        context = {'atos': atos}
        return render(request, 'resultado_pesquisa.html', context)

def boletins_salvos(request):
    boletim = BoletimGerado.objects.all() 

    for b in boletim:
        ato_normativ_index = b.conteudo_pdf.find('AtoNormativ:')
        if ato_normativ_index != -1:
            b.conteudo_pdf = b.conteudo_pdf[ato_normativ_index + len('AtoNormativ:'):]
        else:
            b.conteudo_pdf = b.conteudo_pdf
    return render(request, 'boletins_salvos.html',  {'boletim': boletim})