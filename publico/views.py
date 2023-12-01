from django.shortcuts import render
from core.models import Unidade, Laboratorio, Equipamento, RegimentoInterno, Unidade 
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.db.models import Max
from core.models import Laboratorio,Projeto, Infraestrutura,LaboratorioInfraestrutura,ImagemLaboratorio, Marca, Equipamento, RegimentoInterno, UnidadeAcademica,ImagemInfraestrutura,GrupoDePesquisa,MembroLaboratorio
from django.core.paginator import Paginator

def paginar(list, limit_per_page, request): 
    paginator = Paginator(list, limit_per_page) 
    page = request.GET.get('page')
    atos = paginator.get_page(page)
    context = {'atos': atos}
    return context


def geral(request):
    texto = request.GET.get('filter')
    lab_u = Laboratorio.objects.values('unidade').distinct()
    lab = Laboratorio.objects.all()
    
    if texto:
        laboratorios = Laboratorio.objects.filter(
            nome_laboratorio__icontains=texto 
        )
    else:

        laboratorios = Laboratorio.objects.annotate(max_imagem=Max('imagens__data_upload')).all()

    paginator = Paginator(laboratorios, 6)  
    page = request.GET.get('page')
    laboratorios = paginator.get_page(page)


    context = {
        'lab_u': lab_u,
        'lab': lab,
        'laboratorios': laboratorios,
    }

    return render(request, 'publico.html', context)


def view(request, laboratorio_id):
    laboratorio = get_object_or_404(Laboratorio, id=laboratorio_id)

    regimentos_internos = RegimentoInterno.objects.filter(laboratorio=laboratorio)

    unidades_academicas = UnidadeAcademica.objects.filter(laboratorio=laboratorio)

    infraestruturas = Infraestrutura.objects.filter(laboratorio_id=laboratorio.id).filter(status=True)

    projetos = Projeto.objects.filter(laboratorio=laboratorio)

    membros = MembroLaboratorio.objects.filter(laboratorio=laboratorio)

    grupos_de_pesquisa = laboratorio.grupos_de_pesquisa.all()

    return render(request, 'view_publico.html', {'laboratorio': laboratorio, 'infraestruturas': infraestruturas, 'regimentos_internos': regimentos_internos, 'unidades_academicas': unidades_academicas, 'projetos': projetos, 'membros': membros, 'grupos_de_pesquisa': grupos_de_pesquisa})
