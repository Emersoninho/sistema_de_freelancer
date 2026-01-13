from django.urls import path 
from . import views

urlpatterns = [
    path('encontrar_jobs/', views.encontrar_jobs, name='encontrar_jobs'),
    path('aceitar_job/<int:id>/', views.aceitar_job, name='aceitar_job'),
    path('perfil/', views.perfil, name='perfil'),
    path('enviar_projeto/', views.enviar_projeto, name="enviar_projeto"),
    path('dashboard_cliente/', views.dashboard_cliente, name="dashboard_cliente"),
    path('aprovar_projeto/<int:id>/', views.aprovar_projeto, name="aprovar_projeto"),
    path('recusar_projeto/<int:id>/', views.recusar_projeto, name="recusar_projeto"),
]