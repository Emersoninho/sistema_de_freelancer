from django.db import models
from django.contrib.auth.models import AbstractUser #para o usuario 

class CustomUser(AbstractUser):
    # Definimos escolhas para o tipo de usuário
    CHOICES_TIPO = (
        ('F', 'Freelancer'),
        ('C', 'Cliente')
    )

    # O e-mail agora é único e obrigatório
    email = models.EmailField(unique=True)
    
    # Campos extras para o seu sistema
    tipo = models.CharField(max_length=1, choices=CHOICES_TIPO, default='F')
    telefone = models.CharField(max_length=15, blank=True, null=True)
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)

    # Configuração para login por E-mail
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # O Django ainda exige o username internamente

    def __str__(self):
        return self.email