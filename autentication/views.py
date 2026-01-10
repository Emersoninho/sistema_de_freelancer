from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .utils import fields_are_empty, password_is_valid, cpf_is_valid, phone_is_valid
from django.contrib.auth import get_user_model # usar o usuario costumizado

# Definimos o modelo de usuário logo no início
# Isso faz com que a variável 'User' seja o seu 'CustomUser' do autentication
User = get_user_model()

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        tipo = request.POST.get('tipo') # Padrão Freelancer se não vier nada
        cpf = request.POST.get('cpf')
        telefone = request.POST.get('telefone')

         # Criamos o dicionário para reutilizar nos erros
        dados_preenchidos = {'username': username, 'email': email, 'cpf': cpf, 'telefone': telefone, 'tipo': tipo}

         # 1. Verifica campos vazios (Passamos os nomes amigáveis para o usuário)
        if fields_are_empty(request, 
                            Usuario=username, 
                            Email=email, 
                            CPF=cpf, 
                            Telefone=telefone,
                            tipo=tipo, 
                            Senha=password, 
                            Confirmacao=confirm_password):
            return render(request, 'cadastro.html', dados_preenchidos)
        
        # 2. Verifica regras de senha
        if not password_is_valid(request, password, confirm_password):
            return render(request, 'cadastro.html', dados_preenchidos)
        
        # 3. Verifica se o usuário já existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este nome de usuário já está em uso.')
            return render(request, 'cadastro.html', dados_preenchidos)

        # 4. Verifica se o EMAIL já existe (O mais importante agora!)
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado.')
            return render(request, 'cadastro.html', dados_preenchidos)  

        # 5. Validação de formato de CPF (usando a função do utils)
        if not cpf_is_valid(cpf):
            messages.error(request, 'CPF inválido. Certifique-se de digitar os 11 números.')
            return render(request, 'cadastro.html', dados_preenchidos)

        # 6. Verifique se o CPF já está cadastrado (Muito importante!)
        if User.objects.filter(cpf=cpf).exists():
            messages.error(request, 'Este CPF já está cadastrado no sistema.')
            return render(request, 'cadastro.html', dados_preenchidos)

        # 7. Validação de Telefone
        if not phone_is_valid(telefone):
            messages.error(request, 'Telefone inválido. Use o formato (00) 00000-0000.')
            return render(request, 'cadastro.html', dados_preenchidos)
        # ... dentro da sua view ...
        try:
            # O create_user já faz o hash da senha (criptografia) automaticamente
            novo_usuario = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                tipo=tipo,
                cpf=cpf,
                telefone=telefone,
                
            )
            # Se chegou aqui, deu tudo certo!
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('/') # Ou a sua página de sucesso

        except Exception as e:
            # Se o banco de dados rejeitar algo por algum motivo inesperado
            print(f"Erro interno: {e}") # Para você ver o erro no terminal
            messages.error(request, 'Erro interno do sistema. Tente novamente mais tarde.')
            return render(request, 'cadastro.html', dados_preenchidos)    
