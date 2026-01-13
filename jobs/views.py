from django.shortcuts import render
from .utils import filtrar_jobs
from .models import Jobs

def encontrar_jobs(request):
    if request.method == "GET":
        # Captura os dados do formulário
        preco_minimo = request.GET.get('preco_minimo')
        preco_maximo = request.GET.get('preco_maximo')
        prazo_minimo = request.GET.get('prazo_minimo')
        prazo_maximo = request.GET.get('prazo_maximo')
        categoria = request.GET.get('categoria')

        # Chama a função que criamos no utils.py
        jobs = filtrar_jobs(preco_minimo, preco_maximo, prazo_minimo, prazo_maximo, categoria)

        return render(request, 'encontrar_jobs.html', {'jobs': jobs})