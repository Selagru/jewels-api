from django.db import models
from django.utils import timezone
from items.models import Item


class Deal(models.Model):
    customer = models.ForeignKey('auth.User', related_name='deals', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='deals', on_delete=models.CASCADE)
    total = models.PositiveSmallIntegerField(help_text='итого')
    quantity = models.PositiveSmallIntegerField(default=1, help_text='кол-во')
    date = models.DateTimeField(default=timezone.now, null=True, blank=True, help_text='Время завершения сделки')

    class Meta:
        ordering = ['customer']

    def __str__(self):
        return f'{self.customer} {self.date}'
