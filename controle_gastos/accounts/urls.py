from django.urls import path
from django.contrib.auth.views import LoginView


from . import views

urlpatterns = [
    path('entrar/', LoginView.as_view(), name='login'),
]
