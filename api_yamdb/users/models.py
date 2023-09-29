from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOISES = [
        ('USER', 'user'),
        ('MODER', 'moderator'),
        ('ADMIN', 'admin'),
    ]
    bio = models.TextField(verbose_name='Биография', blank=True)
    role = models.CharField(
        verbose_name='Роль', default='USER',
        max_length=20, choices=ROLE_CHOISES
    )
