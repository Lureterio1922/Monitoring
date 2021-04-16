from django.conf.urls import url

from clients.views import get_clients

urlpatterns = [
    url(r'^get_clients/$', get_clients, name='get_clients'),
]