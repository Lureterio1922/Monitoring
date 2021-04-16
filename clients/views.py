from django.http import JsonResponse

from clients.models import Client, Appointment


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


def get_client_info(request, client_id):
    client = Client.objects.get(id=client_id)
    appointments = Appointment.objects.filter(client=client)
    result = []
    for app in appointments:
        d = {
            "name": app.name,
            "text": app.text,
            "date": app.date,
            "days": app.days,
        }
        result.append(d)
    cl = {
        "latitude": client.latitude,
        "longitude": client.longitude,
        "color": "#ffffff",
        "name": client.name,
        "appointments": result
    }

    return JsonResponse(data=cl, safe=False)