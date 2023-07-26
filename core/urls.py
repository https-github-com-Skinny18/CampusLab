from django.urls import path
from . import views
from .views import edit
from .views import salvar_ato
from .views import view
from .views import editar_ato
# from .views import gerar_pdf
from .views import revisao
from .views import pendentes
from .views import GerarPDFView
from .views import view
from . import views
from core import  views
from .views import boletim
from . import views


urlpatterns = [
    path('', views.aprovados, name='index'),
    path('edit/', views.edit, name='edit'),
    path('ato/<int:ato_id>/', views.view, name='view'),
    path('salvar/', views.salvar_ato, name = 'salvar_ato'),
    path('salvar_boletim/<str:ato_ids>/', views.salvar_boletim, name='salvar_boletim'),
    # path('gerar_pdf/<int:ato_ids>/', GerarPDFView.as_view(), name='gerar_pdf'),
    path('gerar_pdf/<str:ato_ids>/', GerarPDFView.as_view(), name='gerar_pdf'),
    path('gerar_boletim/<str:ato_ids>/<int:boletim_id>/', GerarPDFView.as_view(), name='gerar_boletim'),
    path('ato/<int:ato_ids>/editar/', views.editar_ato, name='editar_ato'),
    path('aprovados/', views.aprovados, name='aprovados'),
    path('rascunhos/', views.rascunhos, name='rascunhos'),
    path('cancelados/', views.cancelados, name='cancelados'),
    path('revisao/', views.revisao, name='revisao'),
    path('pendentes/', views.pendentes, name='pendentes'),
    path('boletim/', views.boletim, name='boletim'),
    path('pesquisar/', views.pesquisar, name='pesquisar'),
    path('boletins_salvos/', views.boletins_salvos, name='boletins_salvos'),


]