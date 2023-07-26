from django.shortcuts import render

def autenticacao(request):
    return render(request, 'authentication.html')

