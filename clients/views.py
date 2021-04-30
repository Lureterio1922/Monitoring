import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from Monitoring.settings import BASE_URL
from clients.models import Client, Appointment, NORMAL, Integration_system_problems, Server_lies


def get_clients(request):
    clients = Client.objects.all()
    result =[]
    for client in clients:
        obj = client.get_dict()
        result.append(obj)
    return JsonResponse(data=result,safe=False)

def check_status(request):
    clients = Client.objects.all()
    for client in clients:
        try:
            url = client.url
            r = requests.get(url)
            if r.status_code == 200:
                client.status = NORMAL
            else:
                client.status = Integration_system_problems
                print("Integration_system_problems")

        except Exception as e:
            print(str(e))
            client.status = Server_lies


    for client in clients:
        client.save()
    return HttpResponse()


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
    cl = client.get_dict()
    cl["appointments"] =result
    return JsonResponse(data=cl, safe=False)


def get_map(request):
    template, context = get_template_context()

    return render(request, template, context)


def get_template_context():
    template = "main.html"
    context = {
        "BASE_URL": BASE_URL
    }
    return template, context