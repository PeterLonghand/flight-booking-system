# Generated by Django 5.1.2 on 2024-11-18 18:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0012_alter_seat_plane_alter_seat_seat_class'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seat',
            name='ticket',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seats', to='flight.ticket'),
        ),
    ]
