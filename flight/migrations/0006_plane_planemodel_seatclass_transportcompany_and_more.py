# Generated by Django 5.1.2 on 2024-11-17 17:21

import datetime
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0005_remove_place_airport_remove_place_country_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plane',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PlaneModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('aisles_eco', models.IntegerField(null=True)),
                ('rows_right_eco', models.IntegerField(null=True)),
                ('rows_left_eco', models.IntegerField(null=True)),
                ('rows_middle_eco', models.IntegerField(null=True)),
                ('row_length_eco', models.IntegerField(null=True)),
                ('aisles_bus', models.IntegerField(null=True)),
                ('rows_left_bus', models.IntegerField(null=True)),
                ('rows_right_bus', models.IntegerField(null=True)),
                ('rows_middle_bus', models.IntegerField(null=True)),
                ('row_length_bus', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SeatClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=8, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransportCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.RemoveField(
            model_name='flight',
            name='depart_day',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='airline',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='arrival_time',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='business_fare',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='depart_time',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='economy_fare',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='first_fare',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='plane',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='booking_date',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='coupon_discount',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='coupon_used',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='flight_adate',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='flight_ddate',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='flight_fare',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='other_charges',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='seat_class',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='status',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='total_fare',
        ),
        migrations.AddField(
            model_name='flight',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='flight',
            name='arrival_datetime',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 2, 0, 0)),
        ),
        migrations.AddField(
            model_name='flight',
            name='business_seat_cost',
            field=models.FloatField(default=1.0),
        ),
        migrations.AddField(
            model_name='flight',
            name='depart_datetime',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 1, 0, 0)),
        ),
        migrations.AddField(
            model_name='flight',
            name='economy_seat_cost',
            field=models.FloatField(default=1.0),
        ),
        migrations.AddField(
            model_name='passenger',
            name='patronymic',
            field=models.CharField(max_length=36, null=True, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='Отчество пассажира'),
        ),
        migrations.AlterField(
            model_name='passenger',
            name='first_name',
            field=models.CharField(max_length=36, validators=[django.core.validators.MinLengthValidator(2)], verbose_name='Имя пассажира'),
        ),
        migrations.AlterField(
            model_name='passenger',
            name='gender',
            field=models.CharField(choices=[('male', 'Мужской'), ('female', 'Женский')], max_length=36, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='passenger',
            name='last_name',
            field=models.CharField(max_length=36, validators=[django.core.validators.MinLengthValidator(2)], verbose_name='Фамилия пассажира'),
        ),
        migrations.AlterField(
            model_name='place',
            name='city',
            field=models.CharField(max_length=25, validators=[django.core.validators.RegexValidator('^[a-zA-Zа-яА-Я\\s\\-]{3,25}$', 'Only letters, spaces, and hyphens allowed.')]),
        ),
        migrations.AlterField(
            model_name='place',
            name='code',
            field=models.CharField(max_length=4, validators=[django.core.validators.RegexValidator('^[a-zA-Zа-яА-Я]{3,4}$', 'Only letters allowed.')]),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='email',
            field=models.EmailField(max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='mobile',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ref_no',
            field=models.CharField(max_length=6, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='firstname',
            field=models.CharField(default='Admin', max_length=36),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='user',
            name='patronymic',
            field=models.CharField(blank=True, max_length=36),
        ),
        migrations.AlterField(
            model_name='user',
            name='phonenumber',
            field=models.CharField(default='00000000000', max_length=18, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{9,15}$', 'Enter a valid phone number.')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='surname',
            field=models.CharField(default='Admin', max_length=36),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
        migrations.AddField(
            model_name='flight',
            name='planeid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='flight.plane'),
        ),
        migrations.AddField(
            model_name='plane',
            name='plane_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.planemodel'),
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available', models.BooleanField(default=True)),
                ('address', models.CharField(max_length=4, null=True)),
                ('plane', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='flight.plane')),
                ('ticket', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seats', to='flight.ticket')),
                ('seat_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.seatclass')),
            ],
        ),
        migrations.AddField(
            model_name='plane',
            name='transport_company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.transportcompany'),
        ),
        migrations.DeleteModel(
            name='Week',
        ),
    ]
