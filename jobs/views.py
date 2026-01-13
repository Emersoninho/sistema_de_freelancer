from django.shortcuts import render, redirect, get_object_or_404
from .utils import filtrar_jobs
from .models import Jobs
from django.contrib import messages

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

def aceitar_job(request, id):
    # 1. Busca o job pelo ID
    job = get_object_or_404(Job, id=id)
    
    # 2. Marca como reservado
    job.reservado = True
    
    # 3. Atribui o freelancer (usuário logado) ao job
    # Certifique-se de que seu model Jobs tenha o campo 'profissional'
    job.profissional = request.user
    
    # 4. Salva no banco de dados
    job.save()
    
    messages.success(request, 'Job aceito com sucesso!')
    return redirect('/jobs/encontrar_jobs/')