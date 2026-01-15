from .models import Jobs
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import Jobs
from datetime import datetime

def filtrar_jobs(preco_minimo, preco_maximo, prazo_minimo, prazo_maximo, categoria):
    jobs = Jobs.objects.filter(reservado=False)

    # --- PREÇO ---
    if preco_minimo:
        try:
            preco_minimo = float(preco_minimo)
            jobs = jobs.filter(preco__gte=preco_minimo)
        except ValueError:
            pass  # ignora se vier errado

    if preco_maximo:
        try:
            preco_maximo = float(preco_maximo)
            jobs = jobs.filter(preco__lte=preco_maximo)
        except ValueError:
            pass

    # --- PRAZO (DATA) ---
    if prazo_minimo:
        try:
            prazo_minimo = datetime.strptime(prazo_minimo, "%Y-%m-%d").date()
            jobs = jobs.filter(prazo_entrega__gte=prazo_minimo)
        except ValueError:
            pass

    if prazo_maximo:
        try:
            prazo_maximo = datetime.strptime(prazo_maximo, "%Y-%m-%d").date()
            jobs = jobs.filter(prazo_entrega__lte=prazo_maximo)
        except ValueError:
            pass

    # --- CATEGORIA ---
    if categoria:
        jobs = jobs.filter(categoria=categoria)

    return jobs


# --- BLOCO DE USUÁRIO (PERFIL) ---
def validar_perfil(username, email, usuario_atual):

    if User.objects.filter(username=username)\
        .exclude(id=usuario_atual.id).exists():
        return False, 'Já existe um usuário com esse nome'

    if User.objects.filter(email=email)\
        .exclude(id=usuario_atual.id).exists():
        return False, 'Já existe um usuário com esse e-mail'

    return True, None
  