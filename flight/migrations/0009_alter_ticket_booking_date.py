# Generated by Django 5.1.2 on 2024-11-18 11:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0008_ticket_booking_date_alter_planemodel_row_length_eco'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='booking_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
