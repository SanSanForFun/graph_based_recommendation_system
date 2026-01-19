from django.utils import timezone

from django.db import models


class Interaction(models.Model):
    """ Модель взаимодействия """
    user = models.CharField(verbose_name='Имя пользователя')
    movie = models.CharField(verbose_name='Просмотренный фильм')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'movie')
        verbose_name = 'Взаимодействие'
        verbose_name_plural = 'Взаимодействия'

    def __str__(self):
        return f"{self.user} - {self.movie}"
