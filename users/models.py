from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    chat_id_tg = models.IntegerField(unique=True, verbose_name='id чата Telegram', **NULLABLE)
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
