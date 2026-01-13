from django.db import models
from django.contrib.auth import get_user_model # para o usuario

# Isso busca automaticamente o seu AbstractUser customizado
User = get_user_model()

class Referencias(models.Model):
    arquivo = models.FileField(upload_to='referencias')

    def __str__(self) -> str:
        return self.arquivo.name
    
class Jobs(models.Model):
    categoria_choices = (
        ('D', 'Design'),
        ('EV', 'Edição de Vídeo')
    )
    status_choices = (
        ('C', 'Em criação'),
        ('AA', 'Aguardando aprovação'),
        ('F', 'Finalizado')
    )
    
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    categoria = models.CharField(max_length=2, choices=categoria_choices, default="D")
    prazo_entrega = models.DateTimeField()
    preco = models.FloatField()
    referencias = models.ManyToManyField(Referencias)
    # Mudança sugerida para evitar erros se o profissional for deletado
    profissional = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reservado = models.BooleanField(default=False)
    # Adicionado choices=status_choices aqui
    status = models.CharField(max_length=2, choices=status_choices, default='AA')
    arquivo_final = models.FileField(null=True, blank=True)
    # Adicione esta linha:
    usuario_postou = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs_postados', null=True, blank=True)
    
    # O campo profissional já existe, mantenha-o:
    profissional = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.titulo    