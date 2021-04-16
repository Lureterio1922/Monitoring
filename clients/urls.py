from django.conf.urls import url

from clients.views import get_clients, get_client_info

urlpatterns = [
    url(r'^get_clients/$', get_clients, name='get_clients'),
    url(r'^get_client_info/([0-9]+)/$', get_client_info, name='get_client_info'),
]