# === core/urls.py ===
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('alunos/', views.aluno_list, name='aluno_list'),
    path('alunos/novo/', views.aluno_form, name='aluno_create'),
    path('alunos/<int:id>/editar/', views.aluno_form, name='aluno_update'),
    
    path('programas/', views.programa_list, name='programa_list'),
    path('programas/novo/', views.programa_form, name='programa_create'),
    path('programas/<int:id>/editar/', views.programa_form, name='programa_update'),
    
    path('orientadores/', views.orientador_list, name='orientador_list'),
    path('orientadores/novo/', views.orientador_form, name='orientador_create'),
    
    path('defesas/', views.defesa_list, name='defesa_list'),
    path('defesas/nova/', views.defesa_form, name='defesa_create'),
    path('defesas/<int:id>/', views.diploma_detail, name='diploma_detail'),
    
    path('diplomas/<int:id>/acao/', views.diploma_acao, name='diploma_acao'),
    path('diplomas/<int:id>/xml/', views.diploma_xml, name='diploma_xml'),
    path('diplomas/<int:id>/log/', views.diploma_log, name='diploma_log'),
    
    path('trocar-papel/', views.trocar_papel, name='trocar_papel'),
]
