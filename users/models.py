from django.db import models
from django.contrib.auth.models import AbstractUser
from tasks.models import Task

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.CharField(max_length=40, verbose_name='email', unique=True)
    fio = models.CharField(max_length=40, verbose_name='fio')
    position = models.CharField(max_length=40, verbose_name='position')
    phone = models.CharField(max_length=20, verbose_name='phone', unique=True, **NULLABLE)
    tasks = models.ManyToManyField(Task, verbose_name='tasks', blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} - {self.fio}"

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
