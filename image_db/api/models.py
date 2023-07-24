from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    User Model
    """
    USER_ROLES = (
        ('user', 'user'),
        ('admin', 'admin'),
    )
    email = models.EmailField(
        max_length=255, unique=True
    )
    username = models.CharField(
        max_length=25, unique=True,
        blank=False, null=False
    )
    confirmation_code = models.IntegerField(
        blank=True, null=True
    )
    role = models.CharField(
        max_length=15, choices=USER_ROLES,
        default='user'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

class Image(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.FileField()

