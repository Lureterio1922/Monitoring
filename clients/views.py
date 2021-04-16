from django.http import JsonResponse

from clients.models import Client


def get_clients(request):
    clients = Client.objects.all()
    result =[]
    for client in clients:
        obj = {
            "latitude":client.latitude,
            "longitude":client.longitude,
            "color":"#ffffff",
            "name":client.name ,
        }
        result.append(obj)
    return JsonResponse(data=result,safe=False)