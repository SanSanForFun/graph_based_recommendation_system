from django.db import models


class Graph(models.Model):
    username = models.CharField(verbose_name='Имя пользователя')
    movie = models.CharField(verbose_name='Просмотренный фильм')
