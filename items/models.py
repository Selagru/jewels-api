from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=50, help_text='Название')
    cost = models.IntegerField(default=100, null=True, help_text='Цена')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
