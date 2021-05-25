from django.db import models
from django.db import models
from django.db.models import Model
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.forms import forms
from django_countries.fields import CountryField


NORMAL = "1"
Server_lies = "2"
Active_orders = "3"
Last_minute_applications = "4"
Integration_system_problems = "5"
WARNING = "6"

STATUS_CHOICES = (
    (NORMAL, "Всё нормально"),
    (Server_lies, "Сервер лежит"),
    (Active_orders, "Активные заявки"),
    (Last_minute_applications, "Горящие заявки"),
    (Integration_system_problems, "Проблемы с системой интеграции"),
    (WARNING, "Предупреждение"),
)

types_operations_system = (
    ('CentOS7',"CentOS7"),
    ('CentOS8',"CentOS8"),
    ('CentOS8-old','CentOS8-old'),
)

def get_color(client):
    if client.status == NORMAL:
        return "#00ff00"
    elif client.status == Server_lies:
        return '#ff0000'
    elif client.status == Active_orders:
        return '#ffd700'
    elif client.status == Last_minute_applications:
        return '#8b0000'
    elif client.status == Integration_system_problems:
        return '#000000'
    elif client.status == WARNING:
        return '#FFFF00'


def get_status_text(client):
    for status in STATUS_CHOICES:
        if client.status == status[0]:
            return status[1]
    return "None"




class Client(Model):
    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    latitude = models.FloatField(verbose_name="Широта", default=0)
    longitude = models.FloatField(verbose_name="Долгота", default=0)
    name = models.CharField(verbose_name="Название", max_length=100, default="")
    url = models.CharField(verbose_name='Ссылка', max_length=1000, default='')
    description = models.TextField(verbose_name='Описание', default='', blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=NORMAL)
    operation_system = models.CharField(max_length=100, choices=STATUS_CHOICES, default=NORMAL)
    country = CountryField()

    def __str__(self):
        return self.name

    def get_dict(self):
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "color": get_color(self),
            "title": self.name,
            "status": self.status,
            "statusText": get_status_text(self),
            "server": self.url,
            "description": self.description,
            "contry": self.country.code,
            "id": self.id,

            'ip': self.url,
            'machineType': self.operation_system
        }

class Appointment(Model):
    class Meta:
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'

    name = models.CharField(verbose_name="Название", max_length=100, default="")
    text = models.TextField(verbose_name='Описание', default='', blank=True)
    date = models.DateField(verbose_name="Дата", default=None, null=True)
    days = models.IntegerField(verbose_name="Количество дней выполнения", default=0)
    client = models.ForeignKey(Client, verbose_name="Клиент", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ClientAppointment(Model):
    class Meta:
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)

    def __str__(self):
        return ''


@receiver(post_save, sender=Appointment)
def appointment_save(sender, instance, **kwargs):
    clien_appointment = ClientAppointment()
    clien_appointment.client = instance.client
    clien_appointment.appointment = instance
    clien_appointment.save()



