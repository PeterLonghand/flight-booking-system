from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.db.models import F, ExpressionWrapper, DurationField, DateTimeField


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
            RegexValidator(r'^\+?1?\d{9,15}$', 'Введите корректный номер телефона.')
        ]
    )
    email = models.EmailField(max_length=64, unique=True, null=False)
    password = models.CharField(max_length=16, null=False)

    def __str__(self):
        return f"{self.id}: {self.firstname} {self.surname}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"



class Place(models.Model):
    city = models.CharField(
        max_length=25,
        validators=[
            RegexValidator(r'^[a-zA-Zа-яА-Я\s\-]{3,25}$', 'Только буквы, пробелы и дефисы')
        ],
        null=False,
        verbose_name="Название города"
    )
    code = models.CharField(
        max_length=4,
        validators=[
            RegexValidator(r'^[a-zA-Zа-яА-Я]{3,4}$', 'Только буквы')
        ],
        null=False,
        unique=True,        
        verbose_name="Код"
    )

    def __str__(self):
        return f"{self.city} ({self.code})"
    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
    


class TransportCompany(models.Model):
    name = models.CharField(max_length=64, null=False, unique=True,
        verbose_name="Название компании")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Авиакомпания"
        verbose_name_plural = "Авиакомпании"


class PlaneModel(models.Model):
    AISLES_CHOICES = [(i, str(i)) for i in range(1, 3)]  # от 1 до 2
    ROWS_CHOICES = [(i, str(i)) for i in range(1, 4)]  # от 1 до 3

    ROWS_MIDDLE_CHOICES = [(i, str(i)) for i in range(0, 4)]  #  от 0 до 3
    #ROW_LENGTH_CHOICES = [(i, str(i)) for i in range(1, 101)]  # Длина ряда

    name = models.CharField(max_length=36, null=False, unique=True,
        verbose_name="Название модели")
    aisles_eco = models.IntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(2)], 
        verbose_name="Проходы в Эконом-классе", choices=AISLES_CHOICES)
    rows_right_eco = models.IntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(3)], 
        verbose_name="Ряды в правой части Эконом-класса", choices=ROWS_CHOICES)
    rows_left_eco = models.IntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(3)], 
        verbose_name="Ряды в левой части Эконом-класса", choices=ROWS_CHOICES)
    rows_middle_eco = models.IntegerField(null=True,validators=[MinValueValidator(0), MaxValueValidator(3)], 
        verbose_name="Ряды в середине Эконом-класса", choices=ROWS_MIDDLE_CHOICES)
    row_length_eco = models.IntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(100)], 
        verbose_name="Длина ряда в Эконом-классе")
    aisles_bus = models.IntegerField(null=True,validators=[MinValueValidator(1), MaxValueValidator(2)],
        verbose_name="Проходы в Бизнес-классе", choices=AISLES_CHOICES)
    rows_left_bus = models.IntegerField(null=True,validators=[MinValueValidator(1), MaxValueValidator(2)], 
        verbose_name="Ряды в левой части Бизнес-класса", choices=ROWS_CHOICES)
    rows_right_bus = models.IntegerField(null=True,validators=[MinValueValidator(1), MaxValueValidator(2)], 
        verbose_name="Ряды в правой части Бизнес-класса", choices=ROWS_CHOICES)
    rows_middle_bus = models.IntegerField(null=True,validators=[MinValueValidator(0), MaxValueValidator(2)], 
        verbose_name="Ряды в середине Бизнес-класса", choices=ROWS_MIDDLE_CHOICES)
    row_length_bus = models.IntegerField(null=True,validators=[MinValueValidator(1), MaxValueValidator(22)], 
        verbose_name="Длина ряда в Бизнес-классе")


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
        if self.total_seats > 200:
            raise ValidationError('Общее количество мест не может превышать 200. Сейчас оно равно {}'.format(self.total_seats))

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Модель самолёта"
        verbose_name_plural = "Модели самолётов"


class Plane(models.Model):
    name = models.CharField(max_length=36, null=False, unique=True,
        verbose_name="Название")
    transport_company = models.ForeignKey(TransportCompany, on_delete=models.CASCADE, 
        verbose_name="Авиакомпания")
    plane_model = models.ForeignKey(PlaneModel, on_delete=models.CASCADE, 
        verbose_name="Модель")

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        print("я открыл save")
        # сохраняем самолёт в бд
        super().save(*args, **kwargs)
        print('я дошёл до сюда')
        # автоматом создаём места
        self.create_seats()

    def create_seats(self):
        if not self.plane_model:
            return
        
        # данные о местах из модели самолёта
        eco_seats = self.plane_model.total_eco_seats
        bus_seats = self.plane_model.total_bus_seats
        rows_eco = self.plane_model.total_rows_eco
        rows_bus = self.plane_model.total_rows_bus
        row_length_eco = self.plane_model.row_length_eco
        row_length_bus = self.plane_model.row_length_bus

        # объекты классов сидений
        eco_class, _ = SeatClass.objects.get_or_create(name="Эконом")
        bus_class, _ = SeatClass.objects.get_or_create(name="Бизнес")

        #  места для эконом класса
        self._create_seat_class(eco_seats, rows_eco, "E", eco_class, row_length_eco)

        # места для бизнес класса
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
    def has_free_eco_seats(self):
        return Seat.objects.filter(plane=self, seat_class__name="Эконом", available=True).exists()

    def has_free_bus_seats(self):
        return Seat.objects.filter(plane=self, seat_class__name="Бизнес", available=True).exists()
    
    def is_available_for_flight(self, depart_datetime, arrival_datetime, origin):
        # Проверяем рейсы с пересечениями по времени и учётом интервала в 1 час
        overlapping_flights = Flight.objects.filter(
            planeid=self,
            active=True,  # Только активные рейсы
            depart_datetime__lt=arrival_datetime + timedelta(hours=1),  # Отправление нового рейса должно быть позже прибытия старого рейса + 1 час
            arrival_datetime__gt=depart_datetime - timedelta(hours=1)  # Прибытие старого рейса должно быть раньше отправления нового рейса - 1 час
        ).exclude(destination=origin)
        return not overlapping_flights.exists()
    class Meta:
        verbose_name = "Самолёт"
        verbose_name_plural = "Самолёты"

def default_depart_datetime():
    # Завтрашняя дата с временем 10:00
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    return tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)

def default_arrival_datetime():
    # Завтрашняя дата с временем 14:00
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    return tomorrow.replace(hour=14, minute=0, second=0, microsecond=0)


class Flight(models.Model):
    code = models.CharField(max_length=6, unique=True, null=False, default="AB1234",verbose_name="Код рейса")
    origin = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="departures",verbose_name="Пункт отправлния")
    destination = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="arrivals",verbose_name="Пункт назначения")
    depart_datetime = models.DateTimeField(null=False, default=default_depart_datetime,verbose_name="Время вылета")
    arrival_datetime = models.DateTimeField(null=False, default=default_arrival_datetime,verbose_name="Время прилета")
    economy_seat_cost = models.FloatField(null=False, default=1000.0,verbose_name="Стоимость эконом-места")
    business_seat_cost = models.FloatField(null=False, default=2000.0,verbose_name="Стоимость бизнес-места")
    active = models.BooleanField(default=True,verbose_name="Действующий")
    planeid = models.ForeignKey(Plane, null=True, on_delete=models.CASCADE,verbose_name="Самолет")

    def check_and_set_active(self):
        if self.depart_datetime <= datetime.now() + timedelta(hours=4):
            self.active = False
            #print("\n\nпоставил False")
        else:
            self.active = True
        if self.arrival_datetime <= datetime.now():
            self.active = False
            for seat in self.planeid.seats.all():
                seat.mark_as_available()

        #print(f"\n\n\nя тута{datetime.now() - timedelta(hours=1)}\n\n\n{self.depart_datetime}")
        self.save()

    @property
    def plane_id(self):
        return self.planeid if self.planeid else None
    
    @property
    def transport_company_name(self):
        return self.planeid.transport_company.name if self.planeid and self.planeid.transport_company else None
    
    @property
    def plane_name(self):
        # название самолета, связанного с этим полетом
        return self.planeid.name if self.planeid else None
    
    @property
    def depart_time(self):
        #только время для depart_datetime
        return self.depart_datetime.time() if self.depart_datetime else None


    @property
    def depart_day(self):
        return self.depart_datetime.date() if self.depart_datetime else None
    
    @property
    def arrival_day(self):
        return self.arrival_datetime.date() if self.arrival_datetime else None
    
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
    
    def clean(self):
    # Проверка времени вылета и прилета
        if self.depart_datetime >= self.arrival_datetime:
            raise ValidationError("Дата и время прибытия должны быть позже даты и времени отправления")

        if self.planeid:
            # Проверка на пересечение рейсов
            overlapping_flights = Flight.objects.filter(
                planeid=self.planeid,
                arrival_datetime__gte=self.depart_datetime - timedelta(hours=1),
                depart_datetime__lte=self.arrival_datetime + timedelta(hours=1)
            ).exclude(pk=self.pk)

            if overlapping_flights.exists():
                raise ValidationError(
                    f"Самолёт '{self.planeid.name}' уже занят другим рейсом в указанный период."
                )

            # Проверка на соответствие города прилёта и города вылета
            previous_flights = Flight.objects.filter(
                planeid=self.planeid
            ).exclude(pk=self.pk)  # Все рейсы самолета, кроме текущего

            """
            if previous_flights.exists():
                # Если есть предыдущие рейсы, проверяем последний прилет
                matching_flights = previous_flights.filter(
                    destination=self.origin,
                    arrival_datetime__lte=self.depart_datetime - timedelta(hours=1)
                )

                if not matching_flights.exists():
                    raise ValidationError(
                        f"Самолёт '{self.planeid.name}' должен находиться в городе {self.origin.city} перед вылетом, "
                        "но до этого он прилетел в другой город или информация о рейсе отсутствует."
                    ) 
            
            else:
                # Первый рейс самолета: проверка пропускается
                print(f"Первый рейс для самолета '{self.planeid.name}'. Проверка на местоположение пропущена.")
            """

            
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.origin} → {self.destination}"

    class Meta:
        verbose_name = "Рейс"
        verbose_name_plural = "Рейсы"
    
class SeatClass(models.Model):
    name = models.CharField(max_length=8, null=True)

    def __str__(self):
        return self.name or "No Seat Class"

    class Meta:
        verbose_name = "Класс обслуживания"
        verbose_name_plural = "Классы обслуживания"


class Seat(models.Model):
    available = models.BooleanField(default=True)
    address = models.CharField(max_length=4, null=True)
    plane = models.ForeignKey(Plane, on_delete=models.CASCADE, null=True, related_name="seats")
    seat_class = models.ForeignKey(SeatClass, on_delete=models.CASCADE, null=True)

    def mark_as_occupied(self):
        """Отметить место как занятое."""
        self.available = False
        self.save()

    def mark_as_available(self):
        """Отметить место как свободное."""
        self.available = True
        self.save()

    def __str__(self):
        plane_info = str(self.plane) if self.plane else "No Plane"
        seat_class_info = str(self.seat_class) if self.seat_class else "No Seat Class"
        address_info = self.address if self.address else "No Address"
        return f"Seat {address_info} in {plane_info} ({seat_class_info})"
    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

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
            ('муж', 'Мужской'),
            ('жен', 'Женский')
        ],
        #null=False,
        verbose_name="Пол"
    )
    seat=models.ForeignKey(Seat, null=True, default=None, related_name="passengers", on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Пассажир: {self.first_name} {self.last_name}, Пол: {self.gender}"
    
    class Meta:
        verbose_name = "Пассажир"
        verbose_name_plural = "Пассажиры"




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
    total_price = models.PositiveIntegerField(default=0)
    

    @property
    def depart_date(self):
        return self.flight.depart_datetime.date()
    @property
    def arrival_date(self):
        return self.flight.arrival_datetime.date()
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
    class Meta:
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"