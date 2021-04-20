from django.db import models
from django.db.models import Model
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

NORMAL = "1"
Server_lies = "2"
Active_orders = "3"
Last_minute_applications = "4"
Integration_system_problems = "5"
WARNING = "6"

class Client(Model):
    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    longitude = models.FloatField(verbose_name="Долгота", default=0)
    latitude = models.FloatField(verbose_name="Широта", default=0)
    name = models.CharField(verbose_name="Название", max_length=100, default="")
    url = models. CharField(verbose_name='Ссылка', max_length=1000, default='')
    description = models.TextField(verbose_name='Описание', default='', blank=True)



    STATUS_CHOICES = (
        (NORMAL, "Всё нормально"),
        (Server_lies, "Сервер лежит"),
        (Active_orders, "Активные заявки"),
        (Last_minute_applications, "Горящие заявки"),
        (Integration_system_problems, "Проблемы с системой интеграции"),
        (WARNING, "Предупреждение"),
    )
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=NORMAL)

    def __str__(self):
        return self.name

class Appointment(Model):
    class Meta:
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'
    name = models.CharField(verbose_name="Название", max_length=100, default="")
    text = models.TextField(verbose_name='Описание', default='', blank=True)
    date = models.DateField(verbose_name="Дата", default=None, null=True)
    days = models.IntegerField(verbose_name="Количество дней выполнения", default=0)
    client = models.ForeignKey(Client,verbose_name="Клиент", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ClientAppointment(Model):
    class Meta:
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment,on_delete=models.CASCADE)

    def __str__(self):
        return ''

@receiver(post_save, sender=Appointment)
def appointment_save(sender, instance, **kwargs):
    clien_appointment = ClientAppointment()
    clien_appointment.client = instance.client
    clien_appointment.appointment = instance
    clien_appointment.save()
