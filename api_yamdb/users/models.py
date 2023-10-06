import random

from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models


class CustomUser(AbstractUser):
    USER_ROLE = 'user'
    MODER_ROLE = 'moderator'
    ADMIN_ROLE = 'admin'
    ROLE_CHOISES = [
        (USER_ROLE, 'user'),
        (MODER_ROLE, 'moderator'),
        (ADMIN_ROLE, 'admin'),
    ]
    bio = models.TextField(verbose_name='Биография', blank=True)
    role = models.CharField(
        verbose_name='Роль', default=USER_ROLE,
        max_length=20, choices=ROLE_CHOISES)

    class Meta:
        ordering = ('username', )

    @property
    def is_user(self):
        return self.role == self.USER_ROLE

    @property
    def is_moderator(self):
        return self.role == self.MODER_ROLE

    @property
    def is_admin(self):
        return (
            self.role == self.ADMIN_ROLE
            or self.is_superuser
            or self.is_staff)
