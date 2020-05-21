from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView


from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('entrar/', LoginView.as_view(), name='login'),
    path('sair/', LogoutView.as_view() , name='logout'),
    path('cadastrese/', views.register, name='register'),
    path('nova-senha/', views.password_reset, name='password_reset'),
    path('confirmar-nova-senha/<key>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('editar/', views.edit, name='edit'),
    path('editar-senha/', views.edit_password, name='edit_password'),

]
