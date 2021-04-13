from django.db import models
from django.db.models import Model

class Client(Model):
    longitude = models.FloatField(verbose_name="Долгота", default=0)
    latitude = models.FloatField(verbose_name="Широта", default=0)
    name = models.CharField(verbose_name="Название", max_length=100, default="")
    url = models. CharField(verbose_name='Ссылка', max_length=1000, default='')

    NORMAL = "1"
    Server_lies = "2"
    Active_orders = "3"
    Last_minute_applications = "4"
    Integration_system_problems = "5"
    Warning = "6"

    STATUS_CHOICES = (
        (NORMAL, "Всё нормально"),
        (Server_lies, "Сервер лежит"),
        (Active_orders, "Активные заявки"),
        (Last_minute_applications, "Горящие заявки"),
        (Integration_system_problems, "Проблемы с системой интеграции"),
        (Warning, "Предупреждение"),
    )
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=NORMAL)

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