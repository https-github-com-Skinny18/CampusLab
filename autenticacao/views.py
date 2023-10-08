from django.shortcuts import render, redirect
from django.contrib import messages
from .ldap_utils import autenticar
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth import get_user_model
from django.contrib import messages


User = get_user_model()


def autenticacao(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = autenticar(email, password)
        if user:
            # Autenticação bem-sucedida
            # Faça o que for necessário aqui, como armazenar informações do usuário na sessão
            request.session['user_id'] = user['dn']  # Exemplo de armazenamento do DN do usuário

            # Verifica se o usuário já existe no banco de dados do Django
            try:
                django_user = User.objects.get(username=email)
            except User.DoesNotExist:
                # Cria um novo usuário no banco de dados do Django
                django_user = User.objects.create_user(username=email)

            # Autentica o usuário no Django
            django_user.backend = 'django_auth_ldap.backend.LDAPBackend'
            login(request, django_user, backend='django_auth_ldap.backend.LDAPBackend')

            return redirect('main')  # Redireciona para a página de 'aprovados' após o login

        else:
            # Autenticação falhou
            messages.error(request, 'Credenciais inválidas')
            

    return render(request, 'authentication.html') 

def deslogar(request):
    
    logout(request)
    return render(request, 'authentication.html')

