# Generated by Django 5.1.2 on 2024-12-06 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0018_remove_seat_ticket_seat_passenger'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seat',
            name='passenger',
        ),
        migrations.AddField(
            model_name='passenger',
            name='seat',
            field=models.ManyToManyField(default=None, null=True, related_name='passengers', to='flight.seat'),
        ),
    ]