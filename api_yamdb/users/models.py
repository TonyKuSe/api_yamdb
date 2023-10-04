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


class EmailVerification(models.Model):
    confirmation_code = models.CharField(max_length=6)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'EmailVerification for {self.user.email}'

    def set_new_confirm_code(self, *args, **kwargs):
        self.confirmation_code = self.generate_confirm_code()
        return self

    def generate_confirm_code(self):
        return random.randint(100_000, 999_999)

    def send_verification_email(self):
        send_mail(
            subject='Код для получения токена',
            message=f'''
                <p>
                    Для получения токена авторизации в API сервиса api_yamdb
                    отправьте POST-запрос с параметрами username
                    и confirmation_code на эндпоинт <i>/api/v1/auth/token/</i>
                    <br>
                    Ваш код подтверждения:
                    <strong>{self.confirmation_code}</strong>
                </p>
            ''',
            from_email='from@example.com',
            recipient_list=[self.user.email],
            fail_silently=False,
        )
