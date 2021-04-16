from clients.models import Client, Appointment


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