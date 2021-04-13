from django.db import models
from django.db.models import Model

class Client(Model):
    longitude = models.FloatField(verbose_name="Долгота", default=0)
    latitude = models.FloatField(verbose_name="Широта", default=0)
    status = models.TextField(verbose_name='Статус', default='') #сделать choises
    name = models.CharField(verbose_name="Название", max_length=100, default="")
    url = models.TextField(verbose_name='Ссылка', default='')

    def __str__(self):
        return self.name

class Appontment(Model):
    name = models.CharField(verbose_name="Название", max_length=100, default="")
    text = models.TextField(verbose_name='Описание', default='', blank=True)
    date = models.DateField(verbose_name="Дата", default=None, null=True)
    days = models.IntegerField(verbose_name="Количество дней выполнения", default=0)
    client = models.CharField(verbose_name="Клиент", max_length=100, default="")

    def __str__(self):
        return self.name