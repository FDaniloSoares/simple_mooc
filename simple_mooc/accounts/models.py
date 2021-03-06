from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core import validators
import re
from django.conf import settings 


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        'Nome de Usuario', max_length=30, unique=True,
        validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'),
        'Nome de usuario so pode conter letras, digitos ou @/./+/-/_', 'invalid' )]
    
    )
    email = models.EmailField('E-mail', unique=True)
    name = models.CharField('Nome', max_length=30, blank=True)
    is_active = models.BooleanField('Esta ativo?', blank=True, default=True)
    is_staff = models.BooleanField('Esta da equipe?', blank=True, default=True)
    date_joined = models.DateTimeField(
        'Data de Entrada', auto_now_add=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.name or self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return str(self)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

class PasswordReset(models.Model):
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuario',on_delete=models.CASCADE,
        related_name='resets'
    )
    key = models.CharField('Chave', max_length=100, unique=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    confirmed = models.BooleanField('Confirmado?', default=False, blank=True)

    def __str__(self):
        return '{0} em {1}'.format(self.user, self.created_at)

    class Meta:
        verbose_name = 'Nova senha'
        verbose_name_plural = 'Novas senhas'
        ordering = ['-created_at']