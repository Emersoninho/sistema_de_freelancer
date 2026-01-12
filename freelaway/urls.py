from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views #urls de recuperação de senha
from django.shortcuts import redirect #url vazia
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('autentication.urls')),
    path('jobs/', include('jobs.urls')),
    
    # Quando a URL for vazia, redireciona para 'cadastro/'
    path('', lambda request: redirect('auth/cadastro/')),

    # 1. Página para digitar o e-mail
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name='password_reset'),
    
    # 2. Mensagem de sucesso (e-mail enviado)
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name='password_reset_done'),
    
    # 3. Link que o usuário clica no e-mail (validação do token)
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    
    # 4. Mensagem de senha alterada com sucesso
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
