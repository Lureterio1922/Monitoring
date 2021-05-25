# Generated by Django 3.1 on 2021-05-25 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_client_operation_system'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='operation_system',
            field=models.CharField(choices=[('CentOS7', 'CentOS7'), ('CentOS8', 'CentOS8'), ('CentOS8-old', 'CentOS8-old')], default='1', max_length=100),
        ),
    ]