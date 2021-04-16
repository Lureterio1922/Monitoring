from django.http import JsonResponse

from clients.models import Client, Appointment, NORMAL, Server_lies, Active_orders, Last_minute_applications, \
    Integration_system_problems, WARNING


def get_color(client):
    if client.status == NORMAL:
        return "#00ff00"
    elif client.status ==Server_lies:
        return '#ff0000'
    elif client.status == Active_orders:
        return '#f08080'
    elif client.status ==Last_minute_applications:
        return '#8b0000'
    elif client.status ==Integration_system_problems:
        return '#000000'
    elif client.status == WARNING:
        return '#FFFF00'



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
        "color": get_color(client),
        "name": client.name,
        "appointments": result
    }

    return JsonResponse(data=cl, safe=False)