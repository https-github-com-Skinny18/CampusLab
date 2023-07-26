from django.urls import path
from autenticacao import views

urlpatterns = [
    path('auth/', views.autenticacao, name='autenticacao'),
]
