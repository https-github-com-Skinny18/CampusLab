from django.urls import path, include
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
from .views import aprovados
from . import views
from core import  views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', views.index, name='index'),
    path('aprovados/', views.aprovados, name='aprovados'),
    path('edit/', views.edit, name='edit'),
    path('ato/<int:ato_id>/',views.view, name='view'),
    path('salvar/', views.salvar_ato, name = 'salvar_ato'),
    path('gerar_pdf/<int:ato_id>/', GerarPDFView.as_view(), name='gerar_pdf'),
    path('ato/<int:ato_id>/editar/', views.editar_ato, name='editar_ato'),
    path('aprovados/', views.aprovados, name='aprovados'),
    path('rascunhos/', views.rascunhos, name='rascunhos'),
    path('cancelados/', views.cancelados, name='cancelados'),
    path('revisao/', views.revisao, name='revisao'),
    path('pendentes/', views.pendentes, name='pendentes'),
]
 # path('gerar_pdf/<int:ato_id>/', views.gerar_pdf, name='gerar_pdf'),