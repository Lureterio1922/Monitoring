# Generated by Django 3.1 on 2021-05-25 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_client_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='operation_system',
            field=models.CharField(choices=[('1', 'Всё нормально'), ('2', 'Сервер лежит'), ('3', 'Активные заявки'), ('4', 'Горящие заявки'), ('5', 'Проблемы с системой интеграции'), ('6', 'Предупреждение')], default='1', max_length=100),
        ),
    ]