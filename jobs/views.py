from django.shortcuts import render, redirect, get_object_or_404
from .utils import filtrar_jobs, validar_perfil
from .models import Jobs
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse

User = get_user_model()

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
    job = get_object_or_404(Jobs, id=id)
    
    # 2. Marca como reservado
    job.reservado = True
    
    # 3. Atribui o freelancer (usuário logado) ao job
    # Certifique-se de que seu model Jobs tenha o campo 'profissional'
    job.profissional = request.user
    
    # 4. Salva no banco de dados
    job.save()
    
    messages.success(request, 'Job aceito com sucesso!')
    return redirect('/jobs/encontrar_jobs/')

def perfil(request):
    if request.method == "GET":
        # Busca apenas os jobs que o usuário logado aceitou
        jobs = Jobs.objects.filter(profissional=request.user)
        return render(request, 'perfil.html', {'jobs': jobs})
    
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')

        # A lógica de validação no utils.py também deve usar o User correto
        valido, mensagem = validar_perfil(username, email, request.user)

        if not valido:
            messages.error(request, mensagem)
            return redirect('/jobs/perfil')

        # Atualizando os dados
        request.user.username = username
        request.user.email = email
        request.user.first_name = primeiro_nome
        request.user.last_name = ultimo_nome
        request.user.save()

        messages.success(request, 'Dados atualizados com sucesso!')
        return redirect('/jobs/perfil')

def enviar_projeto(request):
    arquivo = request.FILES.get('arquivo')
    id_job = request.POST.get('id_job')
    arquivo = request.FILES.get('arquivo') # O arquivo vem daqui!
    
    job = Jobs.objects.get(id=id_job)
    job.arquivo_final = arquivo   # Aqui salva o arquivo no novo campo
    job.status = 'AA'            # Muda o status para o cliente aprovar
    job.save()
    return redirect('/jobs/perfil/')   

def dashboard_cliente(request):
    # Filtra jobs que eu (usuário logado) postei
    meus_jobs = Jobs.objects.filter(usuario_postou=request.user)
    
    return render(request, 'dashboard_cliente.html', {'meus_jobs': meus_jobs})

from django.shortcuts import get_object_or_404, redirect

def aprovar_projeto(request, id):
    job = get_object_or_404(Jobs, id=id)
    
    # Segurança: Apenas o dono do job pode aprovar
    if job.usuario_postou == request.user:
        job.status = 'F'
        job.save()
        return redirect('/jobs/dashboard_cliente/')
    else:
        # Se alguém tentar aprovar um job que não é seu
        return redirect('/jobs/perfil/')    