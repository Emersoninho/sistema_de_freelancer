import re

from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def fields_are_empty(request, **kwargs):
    for key, value in kwargs.items():
        # Primeiro checamos se o valor é None ou se, após converter para string e limpar, está vazio
        if value is None or not str(value).strip():
            messages.error(request, f'O campo {key} não pode estar vazio.')
            return True
    return False

def password_is_valid(request, password, confirm_password):
    # Dicionário de regras para facilitar a leitura
    rules = [
        (len(password) < 6, 'Sua senha deve conter 6 ou mais caracteres'),
        (password != confirm_password, 'As senhas não coincidem!'),
        (not re.search('[A-Z]', password), 'Sua senha não contém letras maiúsculas'),
        (not re.search('[a-z]', password), 'Sua senha não contém letras minúsculas'),
        (not re.search('[0-9]', password), 'Sua senha não contém números'),
        (not re.search(r'[!@#$%^&*(),.?":{}|<>]', password), 'Sua senha não contém caracteres especiais (@, #, etc)'),
    ]

    for condition, error_message in rules:
        if condition:
            messages.error(request, error_message)
            return False

    return True

def email_html(path_template: str, assunto: str, para: list, **kwargs) -> dict:
    
    html_content = render_to_string(path_template, kwargs)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(assunto, text_content, settings.EMAIL_HOST_USER, para)

    email.attach_alternative(html_content, "text/html")
    email.send()
    return {'status': 1}

def email_is_valid(request, email, confirm_email):
    # 1. Verifica se os dois campos são iguais
    if email != confirm_email:
        messages.error(request, 'Os e-mails digitados não coincidem!')
        return False
        
    # 2. Verifica o formato usando o seu Regex
    if not re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        messages.error(request, 'Digite um formato de e-mail válido')
        return False
        
    return True

def cpf_is_valid(cpf):
    # Remove pontos e traços para validar apenas os números
    cpf_limpo = re.sub(r'\D', '', cpf)
    return len(cpf_limpo) == 11

def phone_is_valid(phone):
    # Verifica se tem entre 10 e 11 dígitos (com DDD)
    phone_limpo = re.sub(r'\D', '', phone)
    return 10 <= len(phone_limpo) <= 11    