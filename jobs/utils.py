from .models import Jobs

def filtrar_jobs(preco_minimo, preco_maximo, prazo_minimo, prazo_maximo, categoria):
    # Começamos com os jobs disponíveis
    jobs = Jobs.objects.filter(reservado=False)

    # Aplicamos os filtros apenas se os valores existirem
    if preco_minimo:
        jobs = jobs.filter(preco__gte=preco_minimo)

    if preco_maximo:
        jobs = jobs.filter(preco__lte=preco_maximo)

    if prazo_minimo:
        jobs = jobs.filter(prazo_entrega__gte=prazo_minimo)

    if prazo_maximo:
        jobs = jobs.filter(prazo_entrega__lte=prazo_maximo)    

    if categoria:
        jobs = jobs.filter(categoria=categoria)

    return jobs

# --- BLOCO DE USUÁRIO (PERFIL) ---
def validar_perfil(username, email, usuario_atual):
    if User.objects.filter(username=username).exclude(id=usuario_atual.id).exists():
        return False, 'Já existe um usuário com esse nome'
    
    if User.objects.filter(email=email).exclude(id=usuario_atual.id).exists():
        return False, 'Já existe um usuário com esse E-mail'
    
    return True, None   