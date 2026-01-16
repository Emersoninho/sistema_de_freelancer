from django.shortcuts import render, redirect, get_object_or_404
from .utils import filtrar_jobs, validar_perfil
from .models import Jobs
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.contrib.auth.decorators import login_required # segurança
from django.db import transaction


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

@login_required(login_url='/auth/login') # precisa altera banco de dados
def aceitar_job(request, id):

    # 🚫 Só aceita POST
    if request.method != 'POST':
        return redirect('/jobs/encontrar_jobs/')

    # 🧠 Tudo dentro de uma transação
    with transaction.atomic():

        # 🔒 Lock no job
        job = Jobs.objects.select_for_update().get(id=id)

        # 🚫 Se já estiver reservado
        if job.reservado:
            messages.error(request, 'Este job já foi aceito.')
            return redirect('/jobs/encontrar_jobs/')

        # 🚫 Só freelancer pode aceitar
        if request.user.tipo != 'F':
            messages.error(request, 'Apenas freelancers podem aceitar jobs.')
            return redirect('/jobs/encontrar_jobs/')

        # ✅ Reserva o job
        job.reservado = True
        job.profissional = request.user
        job.save()

    messages.success(request, 'Job aceito com sucesso!')
    return redirect('/jobs/perfil/')

@login_required(login_url='/auth/login')  # precisa altera banco de dados
def perfil(request):
    # 🔐 Bloqueia usuários que NÃO são freelancers
    if request.user.tipo != 'F':
        return redirect('/jobs/dashboard_cliente/')

    if request.method == "GET":
        # Busca apenas os jobs que o usuário logado aceitou
        jobs = Jobs.objects.filter(profissional=request.user)
        return render(request, 'perfil.html', {'jobs': jobs})
    
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')

        valido, mensagem = validar_perfil(username, email, request.user)

        if not valido:
            messages.error(request, mensagem)
            return redirect('/jobs/perfil')

        request.user.username = username
        request.user.email = email
        request.user.first_name = primeiro_nome
        request.user.last_name = ultimo_nome
        request.user.save()

        messages.success(request, 'Dados atualizados com sucesso!')
        return redirect('/jobs/perfil')

@login_required(login_url='/auth/login')  # precisa altera banco de dados
def enviar_projeto(request):
    if request.method != 'POST':
        return redirect('/jobs/perfil/')

    id_job = request.POST.get('id_job')
    arquivo = request.FILES.get('arquivo') # O arquivo vem daqui!
    
    if not arquivo:
        messages.error(request, 'Nenhum arquivo enviado.')
        return redirect('/jobs/perfil/')

    # 🔐 Garante que o job é do freelancer logado
    job = get_object_or_404(
        Jobs,
        id=id_job,
        profissional=request.user
    )

    job.arquivo_final = arquivo
    job.status = 'AA'
    job.save()

    messages.success(request, 'Projeto enviado com sucesso!')
    return redirect('/jobs/perfil/')

@login_required(login_url='/auth/login')  # precisa altera banco de dados
def dashboard_cliente(request):
    # Filtra jobs que eu (usuário logado) postei
    meus_jobs = Jobs.objects.filter(usuario_postou=request.user)
    # Soma o preço apenas dos jobs que estão com status 'F' (Finalizado)
    total_gasto = meus_jobs.filter(status='F').aggregate(Sum('preco'))['preco__sum'] or 0

    return render(request, 'dashboard_cliente.html', {'meus_jobs': meus_jobs, 'total_gasto': total_gasto})

@login_required(login_url='/auth/login') # precisa altera banco de dados
def aprovar_projeto(request, id):

    if request.method != 'POST':
        return redirect('/jobs/dashboard_cliente/')

    job = get_object_or_404(Jobs, id=id)

    if job.usuario_postou != request.user:
        messages.error(request, 'Ação não permitida.')
        return redirect('/jobs/dashboard_cliente/')

    job.status = 'F'
    job.save()

    messages.success(request, 'Projeto aprovado!')
    return redirect('/jobs/dashboard_cliente/')
   

@login_required(login_url='/auth/login')  # precisa altera banco de dados
def recusar_projeto(request, id):
    job = get_object_or_404(Jobs, id=id)

    # Segurança: Apenas o dono pode recusar
    if job.usuario_postou == request.user:
        job.status = "C"  # Volta para 'Em criação'
        job.arquivo_final = None # Remove o arquivo errado
        job.save()
        messages.warning(request, 'Entrega recusada. O projeto voltou para o status de criação.')
    else:
        messages.error(request, 'Ação não permitida.')

    return redirect('/jobs/dashboard_cliente/')        


