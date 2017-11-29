from django.db import models
from django.contrib.auth.models import User


class Action(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name='Действие')
    is_done = models.BooleanField(default=False, verbose_name='Сделано')
    user = models.ForeignKey(User, related_name='user_actions', verbose_name='Пользователь')

    __to_json_fields__ = ('id', 'name', 'is_done')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-is_done']
