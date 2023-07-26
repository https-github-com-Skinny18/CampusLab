from django.urls import path
from autenticacao import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import deslogar

urlpatterns = [
    path('auth/', views.autenticacao, name='autenticacao'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='authentication.html'), name='login'),
    path('deslogar/', deslogar, name='deslogar'),
]
