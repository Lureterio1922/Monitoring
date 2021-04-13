from django.contrib import admin
from django.contrib.admin import StackedInline

from clients.models import Client, Appointment, ClientAppointment


class ClientInlines(StackedInline):
    model = ClientAppointment
    extra = 0
    fields = ["appointment"]

class ClientAdmin(admin.ModelAdmin):
    inlines = (ClientInlines,)



admin.site.register(Client,ClientAdmin)
admin.site.register(Appointment)