from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from django.core.exceptions import ValidationError

from django.db import transaction


# Переработанная модель пользователя
class User(AbstractUser):
    first_name = None
    last_name = None

    firstname = models.CharField(max_length=36, null=False, default="Admin")
    surname = models.CharField(max_length=36, null=False, default="Admin")
    patronymic = models.CharField(max_length=36, blank=True)
    phonenumber = models.CharField(
        max_length=18,
        null=False,
        default="00000000000",
        validators=[
            RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')
        ]
    )
    email = models.EmailField(max_length=64, unique=True, null=False)
    password = models.CharField(max_length=16, null=False)

    def __str__(self):
        return f"{self.id}: {self.firstname} {self.surname}"
    





class Place(models.Model):
    city = models.CharField(
        max_length=25,
        validators=[
            RegexValidator(r'^[a-zA-Zа-яА-Я\s\-]{3,25}$', 'Only letters, spaces, and hyphens allowed.')
        ],
        null=False
    )
    code = models.CharField(
        max_length=4,
        validators=[
            RegexValidator(r'^[a-zA-Zа-яА-Я]{3,4}$', 'Only letters allowed.')
        ],
        null=False
    )

    def __str__(self):
        return f"{self.city} ({self.code})"
    


class TransportCompany(models.Model):
    name = models.CharField(max_length=64, null=False)

    def __str__(self):
        return self.name


class PlaneModel(models.Model):
    name = models.CharField(max_length=20, null=False)
    aisles_eco = models.IntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(2)])
    rows_right_eco = models.IntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(3)])
    rows_left_eco = models.IntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(3)])
    rows_middle_eco = models.IntegerField(null=True,validators=[MinValueValidator(0), MaxValueValidator(3)])
    row_length_eco = models.IntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(100)])
    aisles_bus = models.IntegerField(null=True,validators=[MinValueValidator(1), MaxValueValidator(2)])
    rows_left_bus = models.IntegerField(null=True,validators=[MinValueValidator(1), MaxValueValidator(2)])
    rows_right_bus = models.IntegerField(null=True,validators=[MinValueValidator(1), MaxValueValidator(2)])
    rows_middle_bus = models.IntegerField(null=True,validators=[MinValueValidator(0), MaxValueValidator(2)])
    row_length_bus = models.IntegerField(null=True,validators=[MinValueValidator(1), MaxValueValidator(22)])


    @property
    def total_rows_eco(self):
        return self.rows_right_eco + self.rows_left_eco + self.rows_middle_eco
    
    @property
    def total_rows_bus(self):
        return self.rows_right_bus + self.rows_left_bus + self.rows_middle_bus
    
    @property
    def total_seats(self):
        # общее кол-во мест для эконом и бизнес классов вместе 
        eco_seats = (self.rows_right_eco + self.rows_left_eco + self.rows_middle_eco) * self.row_length_eco
        bus_seats = (self.rows_right_bus + self.rows_left_bus + self.rows_middle_bus) * self.row_length_bus
        return eco_seats + bus_seats
    @property
    def total_eco_seats(self):
        return (self.rows_right_eco + self.rows_left_eco + self.rows_middle_eco) * self.row_length_eco
    
    @property
    def total_bus_seats(self):
        return (self.rows_right_bus + self.rows_left_bus + self.rows_middle_bus) * self.row_length_bus
    
    def clean(self):
        # Проверяем, если общее количество мест больше 200
        if self.total_seats > 200:
            raise ValidationError('Общее количество мест не может превышать 200. Сейчас оно равно {}'.format(self.total_seats))

    def __str__(self):
        return self.name


class Plane(models.Model):
    name = models.CharField(max_length=20, null=False)
    transport_company = models.ForeignKey(TransportCompany, on_delete=models.CASCADE)
    plane_model = models.ForeignKey(PlaneModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        print("я открыл save")
        # Сохраняем самолёт в базе данных
        super().save(*args, **kwargs)
        print('я дошёл до сюда')
        # Автоматически создаём места
        self.create_seats()

    def create_seats(self):
        """
        Создаёт места для текущего самолёта на основе его модели.
        """
        if not self.plane_model:
            return
        
        # Получаем данные о местах из модели самолёта
        eco_seats = self.plane_model.total_eco_seats
        bus_seats = self.plane_model.total_bus_seats
        rows_eco = self.plane_model.total_rows_eco
        rows_bus = self.plane_model.total_rows_bus
        row_length_eco = self.plane_model.row_length_eco
        row_length_bus = self.plane_model.row_length_bus

        # Получаем объекты классов сидений
        eco_class, _ = SeatClass.objects.get_or_create(name="Эконом")
        bus_class, _ = SeatClass.objects.get_or_create(name="Бизнес")

        # Создаём места для эконом класса
        self._create_seat_class(eco_seats, rows_eco, "E", eco_class, row_length_eco)

        # Создаём места для бизнес класса
        self._create_seat_class(bus_seats, rows_bus, "B", bus_class, row_length_bus)

    def _create_seat_class(self, total_seats, rows_per_class, prefix, seat_class, row_length):
        """
        Вспомогательный метод для создания мест определённого класса.
        """
        row_count = rows_per_class
        print(row_length)
        if row_count==1:
            alphabet = "A"
        elif row_count==2:
            alphabet = "AB"
        elif row_count==3:
            alphabet = "ABC"
        elif row_count==4:
            alphabet = "ABCD"
        elif row_count==5:
            alphabet = "ABCDE"
        elif row_count==6:
            alphabet = "ABCDEF"
        elif row_count==7:
            alphabet = "ABCDEFG"
        elif row_count==8:
            alphabet = "ABCDEFGH"
        elif row_count==9:
            alphabet = "ABCDEFGHI"

        with transaction.atomic():
            for row in range(row_length):
                for col in range(rows_per_class):
                    address = f"{prefix}{row}{alphabet[col]}"
                    Seat.objects.create(
                        available=True,
                        address=address,
                        plane=self,
                        seat_class=seat_class
                    )

def default_depart_datetime():
    return datetime(2025, 1, 1, 0, 0)

def default_arrival_datetime():
    return datetime(2025, 1, 2, 0, 0)

class Flight(models.Model):
    code = models.CharField(max_length=6, unique=True, null=False, default="AB1234")
    origin = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="arrivals")
    depart_datetime = models.DateTimeField(null=False, default=datetime(2025, 1, 1, 0, 0))
    arrival_datetime = models.DateTimeField(null=False, default=datetime(2025, 1, 2, 0, 0))
    economy_seat_cost = models.FloatField(null=False, default=1.0)
    business_seat_cost = models.FloatField(null=False, default=1.0)
    active = models.BooleanField(default=True)
    planeid = models.ForeignKey(Plane, null=True, on_delete=models.CASCADE)

    
    
    @property
    def transport_company_name(self):
        # Получаем транспортную компанию, связанная с самолетом
        return self.planeid.transport_company.name if self.planeid and self.planeid.transport_company else None
    
    @property
    def plane_name(self):
        # Получаем название самолета, связанного с этим полетом
        return self.planeid.name if self.planeid else None
    
    @property
    def depart_time(self):
        # Возвращаем только время для depart_datetime
        return self.depart_datetime.time() if self.depart_datetime else None


    @property
    def depart_day(self):
        # Возвращаем только время для depart_datetime
        return self.depart_datetime.date() if self.depart_datetime else None
    
    @property
    def arrival_time(self):
        # Возвращаем только время для arrival_datetime
        return self.arrival_datetime.time() if self.arrival_datetime else None
    
    @property
    def duration(self):
        if self.depart_datetime and self.arrival_datetime:
            duration = self.arrival_datetime - self.depart_datetime
            hours, remainder = divmod(duration.seconds, 3600)  # Получаем количество часов
            minutes, _ = divmod(remainder, 60)  # Получаем количество минут
            return f"{duration.days * 24 + hours} hours, {minutes} minutes"
        return None

    def __str__(self):
        return f"{self.origin} to {self.destination}"

class Passenger(models.Model):
    first_name = models.CharField(
        max_length=36,
        #null=False,
        validators=[MinLengthValidator(2)],
        #default="Имя",
        verbose_name="Имя пассажира"
    )
    last_name = models.CharField(
        max_length=36,
        #null=False,
        validators=[MinLengthValidator(2)],
        verbose_name="Фамилия пассажира"
    )
    patronymic = models.CharField(
        max_length=36,
        null=True,
        validators=[MinLengthValidator(3)],
        verbose_name="Отчество пассажира"
    )
    gender = models.CharField(
        max_length=36,
        choices=[
            ('male', 'Мужской'),
            ('female', 'Женский')
        ],
        #null=False,
        verbose_name="Пол"
    )

    def __str__(self):
        return f"Пассажир: {self.first_name} {self.last_name}, Пол: {self.gender}"




TICKET_STATUS =(
    ('PENDING', 'Pending'),
    ('CONFIRMED', 'Confirmed'),
    ('CANCELLED', 'Cancelled')
)


class Ticket(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="bookings", blank=True, null=True)
    ref_no = models.CharField(max_length=6, unique=True, null=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="tickets", blank=True, null=True)
    mobile = models.CharField(max_length=45, null=True)
    email = models.EmailField(max_length=45, null=True)
    passengers = models.ManyToManyField(Passenger, null=True, default=None, related_name="flight_tickets")
    status = models.CharField(max_length=45, choices=TICKET_STATUS, default='PENDING')
    booking_date = models.DateTimeField(default=datetime.now)

    @property
    def depart_date(self):
        return self.flight.depart_datetime.date()
    @property
    def depart_city(self):
        return self.flight.origin

    @property
    def arrival_city(self):
        return self.flight.destination
    @property
    def transport_company(self):
        return self.flight.transport_company_name
    
    @property
    def plane(self):
        return self.flight.plane_name

    def __str__(self):
        return f"Ticket #{self.id}" if self.id else "No Ticket"



class SeatClass(models.Model):
    name = models.CharField(max_length=8, null=True)

    def __str__(self):
        return self.name or "No Seat Class"


class Seat(models.Model):
    available = models.BooleanField(default=True)
    address = models.CharField(max_length=4, null=True)
    plane = models.ForeignKey(Plane, on_delete=models.CASCADE, null=True, related_name="seats")
    ticket = models.ManyToManyField(Ticket, null=True, default=None, related_name="seats")
    seat_class = models.ForeignKey(SeatClass, on_delete=models.CASCADE, null=True)

    def __str__(self):
        plane_info = str(self.plane) if self.plane else "No Plane"
        seat_class_info = str(self.seat_class) if self.seat_class else "No Seat Class"
        address_info = self.address if self.address else "No Address"
        return f"Seat {address_info} in {plane_info} ({seat_class_info})"







""" from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator

from datetime import datetime

# Create your models here.
class User(AbstractUser):

# Отключаем стандартные поля
    first_name = None
    last_name = None


    username = models.CharField(
        max_length=36,
        unique=True,
        null=False,
        validators=[MinLengthValidator(4)]
    )
    firstname = models.CharField(max_length=36, null=False, validators=[MinLengthValidator(2)],default="DefaultFirstName")
    surname = models.CharField(max_length=36, null=False, validators=[MinLengthValidator(2)],default="DefaultSurname")
    patronymic = models.CharField(max_length=36, blank=True, validators=[MinLengthValidator(3)])
    phonenumber = models.CharField(
        max_length=18,
        null=False,
        validators=[
            MinLengthValidator(7),
            RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')
        ], default="00000000000"
    )
    email = models.EmailField(max_length=64, unique=True, null=False)
    password = models.CharField(max_length=16, null=False, validators=[MinLengthValidator(4)])

    def __str__(self):
        return f"{self.id}: {self.username} ({self.firstname} {self.surname})"

class Place(models.Model):
    city = models.CharField(
        max_length=25,
        validators=[RegexValidator(r'^[a-zA-Zа-яА-Я\s\-]{3,25}$', 'Только буквы, пробелы и тире')],
    )
    #airport = models.CharField(max_length=64)
    code = models.CharField(
        max_length=4,
        validators=[RegexValidator(r'^[a-zA-Zа-яА-Я]{3,4}$', 'Только буквы')],)
    #country = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"


class Week(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.name} ({self.number})"


class Flight(models.Model):
    origin = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="arrivals")
    depart_time = models.TimeField(auto_now=False, auto_now_add=False)
    depart_day = models.ManyToManyField(Week, related_name="flights_of_the_day")
    duration = models.DurationField(null=True)
    arrival_time = models.TimeField(auto_now=False, auto_now_add=False)
    plane = models.CharField(max_length=24)
    airline = models.CharField(max_length=64)
    economy_fare = models.FloatField(null=True)
    business_fare = models.FloatField(null=True)
    first_fare = models.FloatField(null=True)

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"



GENDER = (
    ('male','MALE'),    #(actual_value, human_readable_value)
    ('female','FEMALE')
)

class Passenger(models.Model):
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)

    gender = models.CharField(max_length=20, choices=GENDER, blank=True)
    #passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name="flights")
    #flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="passengers")

    def __str__(self):
        return f"Passenger: {self.first_name} {self.last_name}, {self.gender}"



SEAT_CLASS = (
    ('economy', 'Economy'),
    ('business', 'Business'),
    ('first', 'First')
)

TICKET_STATUS =(
    ('PENDING', 'Pending'),
    ('CONFIRMED', 'Confirmed'),
    ('CANCELLED', 'Cancelled')
)

class Ticket(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="bookings", blank=True, null=True)
    ref_no = models.CharField(max_length=6, unique=True)
    passengers = models.ManyToManyField(Passenger, related_name="flight_tickets")
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="tickets", blank=True, null=True)
    flight_ddate = models.DateField(blank=True, null=True)
    flight_adate = models.DateField(blank=True, null=True)
    flight_fare = models.FloatField(blank=True,null=True)
    other_charges = models.FloatField(blank=True,null=True)
    coupon_used = models.CharField(max_length=15,blank=True)
    coupon_discount = models.FloatField(default=0.0)
    total_fare = models.FloatField(blank=True, null=True)
    seat_class = models.CharField(max_length=20, choices=SEAT_CLASS)
    booking_date = models.DateTimeField(default=datetime.now)
    mobile = models.CharField(max_length=20,blank=True)
    email = models.EmailField(max_length=45, blank=True)
    status = models.CharField(max_length=45, choices=TICKET_STATUS)

    def __str__(self):
        return self.ref_no """


