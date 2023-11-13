from django.db import models
from django_celery_beat.models import PeriodicTask

from users.models import User

NULLABLE = {'blank': True, 'null': True}
PERIOD = [
    ('1', '1 раз в день'),
    ('2', '1 раз в 2 дня'),
    ('3', '1 раз в 3 дня'),
    ('4', '1 раз в 4 дня'),
    ('5', '1 раз в 5 дней'),
    ('6', '1 раз в 6 дней'),
    ('7', '1 раз в 7 дней')
]


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    place = models.CharField(max_length=150, verbose_name='место')
    time = models.TimeField(verbose_name='время')
    action = models.CharField(max_length=300, verbose_name='действие')
    pleasant_habit = models.BooleanField(verbose_name='признак приятной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.DO_NOTHING, verbose_name='связанная привычка',
                                      **NULLABLE)
    frequency = models.CharField(choices=PERIOD, verbose_name='периодичность')
    award = models.CharField(max_length=350, verbose_name='вознаграждение', **NULLABLE)
    time_to_complete = models.PositiveIntegerField(verbose_name='время на выполнение')
    is_published = models.BooleanField(default=False, verbose_name='признак публикации')

    class Meta:
        verbose_name = 'полезная привычка'
        verbose_name_plural = 'полезные привычки'

    def __str__(self):
        return f'{self.place} {self.action} {"- приятная привычка" if self.pleasant_habit else ""}'
