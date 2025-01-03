from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

from datetime import datetime
import math
from .models import *
from capstone.utils import render_to_pdf, createticket

from django.db.models import Exists, OuterRef


from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash

#Fee and Surcharge variable
from .constant import FEE
from flight.utils import addPlaces

try:
    """ if len(Week.objects.all()) == 0:
        createWeekDays()
 """
    if len(Place.objects.all()) == 0:
        addPlaces()

    """ if len(Flight.objects.all()) == 0:
        print("Do you want to add flights in the Database? (y/n)")
        if input().lower() in ['y', 'yes']:
            addDomesticFlights()
            addInternationalFlights() """
except:
    pass

# Create your views here.
from django.http import JsonResponse
from django.db.models import Q
from .models import Place




from django.http import JsonResponse
from django.db.models import Q
from .models import Place



###############################################
def get_places(request, query):
    update_all_flights_status()
    if query == "all":  # Если запрос 'all', возвращаем все города
        places = Place.objects.all()
    else:
        places = Place.objects.filter(Q(city__icontains=query) | Q(code__icontains=query))
    
    place_list = [{'city': place.city, 'code': place.code} for place in places]
    return JsonResponse(place_list, safe=False)


###################################################
""" def get_places(request, query):
    places = Place.objects.filter(Q(city__icontains=query) | Q(code__icontains=query))
    place_list = [{'city': place.city, 'code': place.code} for place in places]

    print(f"Найдено мест: {len(place_list)}")
    return JsonResponse(place_list, safe=False) """

##################################################


def index(request):
    update_all_flights_status()
    min_date = f"{datetime.now().date().year}-{datetime.now().date().month}-{datetime.now().date().day}"
    max_date = f"{datetime.now().date().year if (datetime.now().date().month+3)<=12 else datetime.now().date().year+1}-{(datetime.now().date().month + 3) if (datetime.now().date().month+3)<=12 else (datetime.now().date().month+3-12)}-{datetime.now().date().day}"
    if request.method == 'POST':
        origin = request.POST.get('Origin')
        destination = request.POST.get('Destination')
        depart_date = request.POST.get('DepartDate')
        seat = request.POST.get('SeatClass')
        trip_type = request.POST.get('TripType')
        if(trip_type == '1'):
            return render(request, 'flight/index.html', {
            'origin': origin,
            'destination': destination,
            'depart_date': depart_date,
            'seat': seat.lower(),
            'trip_type': trip_type
        })
        elif(trip_type == '2'):
            return_date = request.POST.get('ReturnDate')
            return render(request, 'flight/index.html', {
            'min_date': min_date,
            'max_date': max_date,
            'origin': origin,
            'destination': destination,
            'depart_date': depart_date,
            'seat': seat.lower(),
            'trip_type': trip_type,
            'return_date': return_date
        })
    else:
        return render(request, 'flight/index.html', {
            'min_date': min_date,
            'max_date': max_date
        })
    
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse

def login_view(request):
    update_all_flights_status()
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        # аутентифицируем
        user = authenticate(request, username=username, password=password)
        
        # если уже существует
        if user is not None:
            login(request, user)
            
            # проверка является ли пользователь суперюзером. если да - перенаправляем на админку
            if user.is_superuser:
                return redirect('/admin/')
            
            # перенаправление на домашнюю страницу для обычного пользователя
            return HttpResponseRedirect(reverse("index"))
        
        # Если учетные данные неверны
        else:
            return render(request, "flight/login.html", {
                "message": "Неправильный логин или пароль."
            })
    else:
        return render(request, "flight/login.html")

@login_required
def account_view(request):
    if request.method == "POST":
        user = request.user
        
        # Update basic information
        user.firstname = request.POST['firstname']
        user.surname = request.POST['lastname']
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.patronymic = request.POST.get('patronymic', '')
        user.phonenumber = request.POST['phonenumber']
        
        # Update password if provided
        password = request.POST.get('password')
        if password:
            confirmation = request.POST.get('confirmation')
            if password != confirmation:
                return JsonResponse({
                    "error": "Passwords must match."
                }, status=400)
            user.set_password(password)
        
        try:
            user.save()
            # If password was changed, need to update session
            if password:
                update_session_auth_hash(request, user)
            return render(request, "flight/my_account.html")

        except Exception as e:
            return JsonResponse({
                "error": "Error updating profile. Username may be taken."
            }, status=400)
    
    return render(request, "flight/my_account.html")


""" def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
            
        else:
            return render(request, "flight/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "flight/login.html")
 """
def register_view(request):
    update_all_flights_status()
    if request.method == "POST":
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        username = request.POST["username"]
        email = request.POST["email"]
        patronymic = request.POST.get("patronymic", "")
        phonenumber = request.POST["phonenumber"]

        # Ensuring password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "flight/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.firstname = fname  # custom field
            user.surname = lname    # custom field
            user.patronymic = patronymic
            user.phonenumber = phonenumber
            user.save()
        except:
            return render(request, "flight/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "flight/register.html")

def logout_view(request):
    update_all_flights_status()
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def query(request, q):
    update_all_flights_status()
    places = Place.objects.all()
    filters = []
    q = q.lower()
    for place in places:
        if (q in place.city.lower()) or (q in place.code.lower()) :
            filters.append(place)
    return JsonResponse([{'code':place.code, 'city':place.city} for place in filters], safe=False)

@csrf_exempt
def flight(request):
    update_all_flights_status()
    print(request.GET)
    trip_type = request.GET.get('TripType')
    o_place = request.GET.get('Origin')
    d_place = request.GET.get('Destination')
    departdate = request.GET.get('DepartDate')
    depart_date = datetime.strptime(departdate, "%Y-%m-%d")
    return_date = None
    """ if trip_type == '2':
        returndate = request.GET.get('ReturnDate')
        return_date = datetime.strptime(returndate, "%Y-%m-%d")
        flightday2 = Week.objects.get(number=return_date.weekday()) ##
        origin2 = Place.objects.get(code=d_place.upper())   ##
        destination2 = Place.objects.get(code=o_place.upper())  ##
     """
    seat = request.GET.get('SeatClass')

    flightday = depart_date ########################################
    destination = Place.objects.get(code=d_place.upper())
    origin = Place.objects.get(code=o_place.upper())
    print(trip_type, o_place, d_place, departdate, seat)
    if seat == 'economy':
        flights = Flight.objects.annotate(has_free_eco_seats=Exists(Seat.objects.filter(plane=OuterRef('planeid'),seat_class__name="Эконом",available=True))).filter(depart_datetime__date=flightday,origin=origin,destination=destination,has_free_eco_seats=True,active=True).order_by('economy_seat_cost')#print("урааа")
        #flights = [flight for flight in flights if flight.has_free_eco_seats]
        print(flights)
        try:
            max_price = flights.last().economy_seat_cost
            min_price = flights.first().economy_seat_cost
            #print('еееееееееееееееееееееее')
            print(max_price, min_price)
        except:
            max_price = 0
            min_price = 0
            print(max_price, min_price)

        """ if trip_type == '2':    ##
            flights2 = Flight.objects.filter(depart_day=flightday2,origin=origin2,destination=destination2).exclude(economy_seat_cost=0).order_by('economy_seat_cost')    ##
            try:
                max_price2 = flights2.last().economy_fare   ##
                min_price2 = flights2.first().economy_fare  ##
            except:
                max_price2 = 0  ##
                min_price2 = 0  ##
         """        
    elif seat == 'business':
        flights = Flight.objects.annotate(has_free_bus_seats=Exists(Seat.objects.filter(plane=OuterRef('planeid'),seat_class__name="Бизнес",available=True))).filter(depart_datetime__date=flightday,origin=origin,destination=destination,has_free_bus_seats=True,active=True).order_by('business_seat_cost')
        try:
            max_price = flights.last().business_seat_cost
            min_price = flights.first().business_seat_cost
        except:
            max_price = 0
            min_price = 0

        """ if trip_type == '2':    ##
            flights2 = Flight.objects.filter(depart_day=flightday2,origin=origin2,destination=destination2).exclude(business_fare=0).order_by('business_fare')    ##
            try:
                max_price2 = flights2.last().business_fare   ##
                min_price2 = flights2.first().business_fare  ##
            except:
                max_price2 = 0  ##
                min_price2 = 0  ##
 """
    """ elif seat == 'first':
        flights = Flight.objects.filter(depart_day=flightday,origin=origin,destination=destination).exclude(first_fare=0).order_by('first_fare')
        try:
            max_price = flights.last().first_fare
            min_price = flights.first().first_fare
        except:
            max_price = 0
            min_price = 0
     """ 
    #       
    """    if trip_type == '2':    ##
            flights2 = Flight.objects.filter(depart_day=flightday2,origin=origin2,destination=destination2).exclude(first_fare=0).order_by('first_fare')
            try:
                max_price2 = flights2.last().first_fare   ##
                min_price2 = flights2.first().first_fare  ##
            except:
                max_price2 = 0  ##
                min_price2 = 0  ##    ##
 """
    #print(calendar.day_name[depart_date.weekday()])
    """ if trip_type == '2':
        return render(request, "flight/search.html", {
            'flights': flights,
            'origin': origin,
            'destination': destination,
            'flights2': flights,   ##
            'origin2': origin,    ##
            'destination2': destination,    ##
            'seat': seat.capitalize(),
            'trip_type': trip_type,
            'depart_date': depart_date,
            'return_date': return_date,
            'max_price': math.ceil(max_price/100)*100,
            'min_price': math.floor(min_price/100)*100,
            'max_price2': math.ceil(max_price/100)*100,    ##
            'min_price2': math.floor(min_price/100)*100    ##
        })
    else: """
    return render(request, "flight/search.html", {
        'flights': flights,
        'origin': origin,
        'destination': destination,
        'seat': seat.capitalize(),
        'trip_type': trip_type,
        'depart_date': depart_date,
        'return_date': return_date,
        'max_price': math.ceil(max_price/100)*100,
        'min_price': math.floor(min_price/100)*100
    })

def review(request):
    update_all_flights_status()
    flight_1 = request.GET.get('flight1Id')
    datetime_str = request.GET.get('flight1Datetime')  # Получаем полную строку даты и времени
    seat = request.GET.get('seatClass')
    round_trip = False

    if request.user.is_authenticated:
        # Находим рейс
        flight1 = Flight.objects.get(id=flight_1)

        # Преобразуем строку в объект datetime
        flight1ddate = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S")

        # Вычисляем дату прибытия на основе модели
        flight1adate = flight1.arrival_datetime

        return render(request, "flight/book.html", {
            'flight1': flight1,
            "flight1ddate": flight1ddate,
            "flight1adate": flight1adate,
            "seat": seat,
            "fee": FEE,
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def book(request):
    update_all_flights_status()
    if request.method == 'POST':
        print(request.POST)
        if request.user.is_authenticated:
            totalprice = 0
            flight_1 = request.POST.get('flight1')
            flight_1date = request.POST.get('flight1Date')
            flight_1class = request.POST.get('flight1Class')
            f2 = False
            """ 
            if request.POST.get('flight2'):
                flight_2 = request.POST.get('flight2')
                flight_2date = request.POST.get('flight2Date')
                flight_2class = request.POST.get('flight2Class')
                f2 = True """
            countrycode = request.POST['countryCode']
            mobile = request.POST['mobile']
            email = request.POST['email']
            flight1 = Flight.objects.get(id=flight_1)
            """ if f2:
                flight2 = Flight.objects.get(id=flight_2) """
            passengerscount = request.POST['passengersCount']
            passengers=[]
            seats=[]
            for i in range(1,int(passengerscount)+1):
                fname = request.POST[f'passenger{i}FName']
                lname = request.POST[f'passenger{i}LName']
                patronymic = request.POST[f'passenger{i}Patronymic']
                gender = request.POST[f'passenger{i}Gender']
                # START логика бронирования места
                seat_address=request.POST[f'passenger{i}Seat']     
                plane_plane = flight1.planeid
                seat_id = Seat.objects.get(address=seat_address, plane=plane_plane)
                seat_id.mark_as_occupied()
                seats.append(seat_id)
                price=request.POST[f'passenger{i}Price']
                totalprice+=int(price)

                # END логика бронирования места
                passengers.append(Passenger.objects.create(first_name=fname,last_name=lname,patronymic=patronymic,gender=gender.lower(),seat=seat_id,price=price))
            coupon = request.POST.get('coupon')
            
            try:
                print("зашёл в try")
                ticket1 = createticket(request.user,passengers,passengerscount,flight1,flight_1date,flight_1class,coupon,countrycode,email,mobile,totalprice)
                if f2:
                    ticket2 = createticket(request.user,passengers,passengerscount,flight2,flight_2date,flight_2class,coupon,countrycode,email,mobile)
                print("вышел из try")
                if(flight_1class == 'Economy'):
                    if f2:
                        fare = (flight1.economy_seat_cost*int(passengerscount))+(flight2.economy_seat_cost*int(passengerscount))
                    else:
                        fare = flight1.economy_seat_cost*int(passengerscount)
                elif (flight_1class == 'Business'):
                    if f2:
                        fare = (flight1.business_seat_cost*int(passengerscount))+(flight2.business_seat_cost*int(passengerscount))
                    else:
                        fare = flight1.business_seat_cost*int(passengerscount)
                elif (flight_1class == 'First'):
                    if f2:
                        fare = (flight1.first_fare*int(passengerscount))+(flight2.first_fare*int(passengerscount))
                    else:
                        fare = flight1.first_fare*int(passengerscount)
            except Exception as e:
                return HttpResponse(e)
            

            if f2:    ##
                return render(request, "flight/payment.html", { ##
                    'fare': totalprice,   ##
                    'ticket': ticket1.id,   ##
                    'ticket2': ticket2.id   ##
                })  ##
            
            print('привет из bookkkk')
            return render(request, "flight/payment.html", {
                'fare': totalprice,
                'ticket': ticket1.id
            })
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponse("Method must be post.")

def payment(request):
    update_all_flights_status()
    print('привет из payment')
    if request.user.is_authenticated:
        #if request.method == 'POST':
            ticket_id = request.POST['ticket']
            t2 = False
            #if request.POST.get('ticket2'):
             #   ticket2_id = request.POST['ticket2']
              #  t2 = True
            """ fare = request.POST.get('fare')
            card_number = request.POST['cardNumber']
            card_holder_name = request.POST['cardHolderName']
            exp_month = request.POST['expMonth']
            exp_year = request.POST['expYear']
            cvv = request.POST['cvv']
 """
            try:
                ticket = Ticket.objects.get(id=ticket_id)
                ticket.status = 'CONFIRMED'
                ticket.booking_date = datetime.now()
                ticket.save()
                if t2:
                    ticket2 = Ticket.objects.get(id=ticket2_id)
                    ticket2.status = 'CONFIRMED'
                    ticket2.save()
                    return render(request, 'flight/payment_process.html', {
                        'ticket1': ticket,
                        'ticket2': ticket2
                    })
                return render(request, 'flight/payment_process.html', {
                    'ticket1': ticket,
                    'ticket2': ""
                })
            except Exception as e:
                return HttpResponse(e)
        #else:
         #   return HttpResponse("Method must be post.")
    else:
        return HttpResponseRedirect(reverse('login'))


def ticket_data(request, ref):
    update_all_flights_status()
    ticket = Ticket.objects.get(ref_no=ref)
    return JsonResponse({
        'ref': ticket.ref_no,
        'from': ticket.flight.origin.code,
        'to': ticket.flight.destination.code,
        'flight_date': ticket.depart_date,
        'status': ticket.status
    })

@csrf_exempt
def get_ticket(request):
    update_all_flights_status()
    ref = request.GET.get("ref")
    ticket1 = Ticket.objects.get(ref_no=ref)
    data = {
        'ticket1':ticket1,
        'current_year': datetime.now().year
    }
    pdf = render_to_pdf('flight/ticket.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


def bookings(request):
    update_all_flights_status()
    if request.user.is_authenticated:
        tickets = Ticket.objects.filter(user=request.user).order_by('-booking_date')
        return render(request, 'flight/bookings.html', {
            'page': 'bookings',
            'tickets': tickets
        })
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def cancel_ticket(request):
    if request.method == "POST":
        ref_no = request.POST.get("ref")
        try:
            ticket = Ticket.objects.get(ref_no=ref_no)
            time_to_flight = ticket.flight.depart_datetime - datetime.now()
            if time_to_flight <= timedelta(hours=6):
                print("\n\nай ай\n")
                return JsonResponse({
                    "success": False,
                    "error": "Бронирование нельзя отменить менее чем за 6 часов до рейса."
                })
            ticket.status = 'CANCELLED'
            ticket.save()
            for passenger in ticket.passengers.all():
                passenger.seat.mark_as_available()
            return JsonResponse({'success': True})
        except Ticket.DoesNotExist:
            return JsonResponse({
                "success": False,
                "error": "Билет не найден."
            })
    return JsonResponse({"success": False, "error": "Некорректный запрос."})   

def resume_booking(request):
    update_all_flights_status()
    if request.method == 'POST':
        if request.user.is_authenticated:
            ref = request.POST['ref']
            ticket = Ticket.objects.get(ref_no=ref)
            if ticket.user == request.user:
                return render(request, "flight/payment.html", {
                    'fare': ticket.total_price,
                    'ticket': ticket.id
                })
            else:
                return HttpResponse("User unauthorised")
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponse("Method must be post.")

def contact(request):
    update_all_flights_status()
    return render(request, 'flight/contact.html')

def privacy_policy(request):
    update_all_flights_status()
    return render(request, 'flight/privacy-policy.html')

def terms_and_conditions(request):
    update_all_flights_status()
    return render(request, 'flight/terms.html')

def about_us(request):
    update_all_flights_status()
    return render(request, 'flight/about.html')

def about_system(request):
    update_all_flights_status()
    return render(request, 'flight/about_system.html')

def about_devs(request):
    update_all_flights_status()
    return render(request, 'flight/about_devs.html')


###############################

def get_seat_map(request, plane_id):
    update_all_flights_status()
    print(f'еееее{plane_id}')
    plane = Plane.objects.get(id=plane_id)
    plane_model = plane.plane_model
    seats = list(plane.seats.values("address", "available"))

    return JsonResponse({
        "planeModel": {
            "row_length_eco": plane_model.row_length_eco,
            "rows_left_eco": plane_model.rows_left_eco,
            "rows_middle_eco": plane_model.rows_middle_eco,
            "rows_right_eco": plane_model.rows_right_eco,
            "row_length_bus": plane_model.row_length_bus,
            "rows_left_bus": plane_model.rows_left_bus,
            "rows_middle_bus": plane_model.rows_middle_bus,
            "rows_right_bus": plane_model.rows_right_bus,
        },
        "seats": seats,
    })
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Flight

def get_plane_id(request, flight_id):
    update_all_flights_status()
    flight = get_object_or_404(Flight, pk=flight_id)
    if flight.planeid:
        print(f'айдишник: {flight.planeid.id}')
        return JsonResponse({"plane_id": flight.planeid.id})
    return JsonResponse({"error": "Plane not assigned to flight"}, status=404)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def mark_seat_occupied(request):
    update_all_flights_status()
    if request.method == 'POST':
        try:
            address = request.GET.get('address')  # Получаем параметр address
            flight_id = request.GET.get('flight')
            # Получаем рейс
            flight = Flight.objects.get(id=flight_id)
            plane = flight.planeid  # Предположим, что у Flight есть ForeignKey на Plane

            # Находим место по address и plane
            seat = Seat.objects.get(address=address, plane=plane)

            # Отмечаем место как занятое (например)
            seat.available = False
            seat.save()

            return JsonResponse({'status': 'success', 'seat_id': seat.id})
        except Flight.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Рейс не найден'}, status=404)
        except Seat.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Место не найдено'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Неподдерживаемый метод'}, status=405)

@csrf_exempt
def mark_seat_available(request, seat_id):
    update_all_flights_status()
    if request.method == "POST":
        try:
            seat = Seat.objects.get(id=seat_id)
            seat.mark_as_available()
            return JsonResponse({"success": True})
        except Seat.DoesNotExist:
            return JsonResponse({"error": "Seat not found."}, status=404)
    return JsonResponse({"error": "Invalid request method."}, status=400)

def get_eco_price(request, flight_id):
    update_all_flights_status()
    print("привет из get_eco_price")
    flight = Flight.objects.get(id=flight_id)
    if flight.economy_seat_cost:
        print(f'eco seat cost: {flight.economy_seat_cost}')
        return JsonResponse({"eco_seat_cost": flight.economy_seat_cost})
    return JsonResponse({"error": "Цена отсутствует"}, status=400)
def get_bus_price(request, flight_id):
    update_all_flights_status()
    print(f"айдиииии {flight_id}")
    flight = Flight.objects.get(id=flight_id)
    if flight.business_seat_cost:
        print(f'bus seat cost: {flight.business_seat_cost}')
        return JsonResponse({"bus_seat_cost": flight.business_seat_cost})

def update_all_flights_status():
    flights = Flight.objects.all()
    for flight in flights:
        flight.check_and_set_active()

""" from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

from datetime import datetime
import math
from .models import *
from capstone.utils import render_to_pdf, createticket


from django.db.models import Q


#Fee and Surcharge variable
from .constant import FEE
from flight.utils import createWeekDays, addPlaces, addDomesticFlights, addInternationalFlights

try:
    if len(Week.objects.all()) == 0:
        createWeekDays()

    if len(Place.objects.all()) == 0:
        addPlaces()

    if len(Flight.objects.all()) == 0:
        print("Do you want to add flights in the Database? (y/n)")
        if input().lower() in ['y', 'yes']:
            addDomesticFlights()
            addInternationalFlights()
except:
    pass

# Create your views here.
from django.http import JsonResponse
from django.db.models import Q
from .models import Place




from django.http import JsonResponse
from django.db.models import Q
from .models import Place



###############################################
def get_places(request, query):
    if query == "all":  # Если запрос 'all', возвращаем все города
        places = Place.objects.all()
    else:
        places = Place.objects.filter(Q(city__icontains=query) | Q(code__icontains=query))
    
    place_list = [{'city': place.city, 'code': place.code} for place in places]
    return JsonResponse(place_list, safe=False)


###################################################
""" """ def get_places(request, query):
    places = Place.objects.filter(Q(city__icontains=query) | Q(code__icontains=query))
    place_list = [{'city': place.city, 'code': place.code} for place in places]

    print(f"Найдено мест: {len(place_list)}")
    return JsonResponse(place_list, safe=False) """ """

##################################################


def index(request):
    min_date = f"{datetime.now().date().year}-{datetime.now().date().month}-{datetime.now().date().day}"
    max_date = f"{datetime.now().date().year if (datetime.now().date().month+3)<=12 else datetime.now().date().year+1}-{(datetime.now().date().month + 3) if (datetime.now().date().month+3)<=12 else (datetime.now().date().month+3-12)}-{datetime.now().date().day}"
    if request.method == 'POST':
        origin = request.POST.get('Origin')
        destination = request.POST.get('Destination')
        depart_date = request.POST.get('DepartDate')
        seat = request.POST.get('SeatClass')
        trip_type = request.POST.get('TripType')
        if(trip_type == '1'):
            return render(request, 'flight/index.html', {
            'origin': origin,
            'destination': destination,
            'depart_date': depart_date,
            'seat': seat.lower(),
            'trip_type': trip_type
        })
        elif(trip_type == '2'):
            return_date = request.POST.get('ReturnDate')
            return render(request, 'flight/index.html', {
            'min_date': min_date,
            'max_date': max_date,
            'origin': origin,
            'destination': destination,
            'depart_date': depart_date,
            'seat': seat.lower(),
            'trip_type': trip_type,
            'return_date': return_date
        })
    else:
        return render(request, 'flight/index.html', {
            'min_date': min_date,
            'max_date': max_date
        })
    
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        # аутентифицируем
        user = authenticate(request, username=username, password=password)
        
        # если уже существует
        if user is not None:
            login(request, user)
            
            # проверка является ли пользователь суперюзером. если да - перенаправляем на админку
            if user.is_superuser:
                return redirect('/admin/')
            
            # перенаправление на домашнюю страницу для обычного пользователя
            return HttpResponseRedirect(reverse("index"))
        
        # Если учетные данные неверны
        else:
            return render(request, "flight/login.html", {
                "message": "Неправильный логин или пароль."
            })
    else:
        return render(request, "flight/login.html")




""" """ def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
            
        else:
            return render(request, "flight/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "flight/login.html")
 """ """
def register_view(request):
    if request.method == "POST":
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        username = request.POST["username"]
        email = request.POST["email"]
        patronymic = request.POST.get("patronymic", "")
        phonenumber = request.POST["phonenumber"]

        # Ensuring password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "flight/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.firstname = fname  # custom field
            user.surname = lname    # custom field
            user.patronymic = patronymic
            user.phonenumber = phonenumber
            user.save()
        except:
            return render(request, "flight/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "flight/register.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def query(request, q):
    places = Place.objects.all()
    filters = []
    q = q.lower()
    for place in places:
        if (q in place.city.lower()) or (q in place.code.lower()) :
            filters.append(place)
    return JsonResponse([{'code':place.code, 'city':place.city} for place in filters], safe=False)

@csrf_exempt
def flight(request):
    o_place = request.GET.get('Origin')
    d_place = request.GET.get('Destination')
    trip_type = request.GET.get('TripType')
    departdate = request.GET.get('DepartDate')
    depart_date = datetime.strptime(departdate, "%Y-%m-%d")
    return_date = None
    if trip_type == '2':
        returndate = request.GET.get('ReturnDate')
        return_date = datetime.strptime(returndate, "%Y-%m-%d")
        flightday2 = Week.objects.get(number=return_date.weekday()) ##
        origin2 = Place.objects.get(code=d_place.upper())   ##
        destination2 = Place.objects.get(code=o_place.upper())  ##
    seat = request.GET.get('SeatClass')

    flightday = Week.objects.get(number=depart_date.weekday())
    destination = Place.objects.get(code=d_place.upper())
    origin = Place.objects.get(code=o_place.upper())
    if seat == 'economy':
        flights = Flight.objects.filter(depart_day=flightday,origin=origin,destination=destination).exclude(economy_fare=0).order_by('economy_fare')
        try:
            max_price = flights.last().economy_fare
            min_price = flights.first().economy_fare
        except:
            max_price = 0
            min_price = 0

        if trip_type == '2':    ##
            flights2 = Flight.objects.filter(depart_day=flightday2,origin=origin2,destination=destination2).exclude(economy_fare=0).order_by('economy_fare')    ##
            try:
                max_price2 = flights2.last().economy_fare   ##
                min_price2 = flights2.first().economy_fare  ##
            except:
                max_price2 = 0  ##
                min_price2 = 0  ##
                
    elif seat == 'business':
        flights = Flight.objects.filter(depart_day=flightday,origin=origin,destination=destination).exclude(business_fare=0).order_by('business_fare')
        try:
            max_price = flights.last().business_fare
            min_price = flights.first().business_fare
        except:
            max_price = 0
            min_price = 0

        if trip_type == '2':    ##
            flights2 = Flight.objects.filter(depart_day=flightday2,origin=origin2,destination=destination2).exclude(business_fare=0).order_by('business_fare')    ##
            try:
                max_price2 = flights2.last().business_fare   ##
                min_price2 = flights2.first().business_fare  ##
            except:
                max_price2 = 0  ##
                min_price2 = 0  ##

    elif seat == 'first':
        flights = Flight.objects.filter(depart_day=flightday,origin=origin,destination=destination).exclude(first_fare=0).order_by('first_fare')
        try:
            max_price = flights.last().first_fare
            min_price = flights.first().first_fare
        except:
            max_price = 0
            min_price = 0
            
        if trip_type == '2':    ##
            flights2 = Flight.objects.filter(depart_day=flightday2,origin=origin2,destination=destination2).exclude(first_fare=0).order_by('first_fare')
            try:
                max_price2 = flights2.last().first_fare   ##
                min_price2 = flights2.first().first_fare  ##
            except:
                max_price2 = 0  ##
                min_price2 = 0  ##    ##

    #print(calendar.day_name[depart_date.weekday()])
    if trip_type == '2':
        return render(request, "flight/search.html", {
            'flights': flights,
            'origin': origin,
            'destination': destination,
            'flights2': flights2,   ##
            'origin2': origin2,    ##
            'destination2': destination2,    ##
            'seat': seat.capitalize(),
            'trip_type': trip_type,
            'depart_date': depart_date,
            'return_date': return_date,
            'max_price': math.ceil(max_price/100)*100,
            'min_price': math.floor(min_price/100)*100,
            'max_price2': math.ceil(max_price2/100)*100,    ##
            'min_price2': math.floor(min_price2/100)*100    ##
        })
    else:
        return render(request, "flight/search.html", {
            'flights': flights,
            'origin': origin,
            'destination': destination,
            'seat': seat.capitalize(),
            'trip_type': trip_type,
            'depart_date': depart_date,
            'return_date': return_date,
            'max_price': math.ceil(max_price/100)*100,
            'min_price': math.floor(min_price/100)*100
        })

def review(request):
    flight_1 = request.GET.get('flight1Id')
    date1 = request.GET.get('flight1Date')
    seat = request.GET.get('seatClass')
    round_trip = False
    if request.GET.get('flight2Id'):
        round_trip = True

    if round_trip:
        flight_2 = request.GET.get('flight2Id')
        date2 = request.GET.get('flight2Date')

    if request.user.is_authenticated:
        flight1 = Flight.objects.get(id=flight_1)
        flight1ddate = datetime(int(date1.split('-')[2]),int(date1.split('-')[1]),int(date1.split('-')[0]),flight1.depart_time.hour,flight1.depart_time.minute)
        flight1adate = (flight1ddate + flight1.duration)
        flight2 = None
        flight2ddate = None
        flight2adate = None
        if round_trip:
            flight2 = Flight.objects.get(id=flight_2)
            flight2ddate = datetime(int(date2.split('-')[2]),int(date2.split('-')[1]),int(date2.split('-')[0]),flight2.depart_time.hour,flight2.depart_time.minute)
            flight2adate = (flight2ddate + flight2.duration)
        #print("//////////////////////////////////")
        #print(f"flight1ddate: {flight1adate-flight1ddate}")
        #print("//////////////////////////////////")
        if round_trip:
            return render(request, "flight/book.html", {
                'flight1': flight1,
                'flight2': flight2,
                "flight1ddate": flight1ddate,
                "flight1adate": flight1adate,
                "flight2ddate": flight2ddate,
                "flight2adate": flight2adate,
                "seat": seat,
                "fee": FEE
            })
        return render(request, "flight/book.html", {
            'flight1': flight1,
            "flight1ddate": flight1ddate,
            "flight1adate": flight1adate,
            "seat": seat,
            "fee": FEE
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def book(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            flight_1 = request.POST.get('flight1')
            flight_1date = request.POST.get('flight1Date')
            flight_1class = request.POST.get('flight1Class')
            f2 = False
            if request.POST.get('flight2'):
                flight_2 = request.POST.get('flight2')
                flight_2date = request.POST.get('flight2Date')
                flight_2class = request.POST.get('flight2Class')
                f2 = True
            countrycode = request.POST['countryCode']
            mobile = request.POST['mobile']
            email = request.POST['email']
            flight1 = Flight.objects.get(id=flight_1)
            if f2:
                flight2 = Flight.objects.get(id=flight_2)
            passengerscount = request.POST['passengersCount']
            passengers=[]
            for i in range(1,int(passengerscount)+1):
                fname = request.POST[f'passenger{i}FName']
                lname = request.POST[f'passenger{i}LName']
                gender = request.POST[f'passenger{i}Gender']
                passengers.append(Passenger.objects.create(first_name=fname,last_name=lname,gender=gender.lower()))
            coupon = request.POST.get('coupon')
            
            try:
                ticket1 = createticket(request.user,passengers,passengerscount,flight1,flight_1date,flight_1class,coupon,countrycode,email,mobile)
                if f2:
                    ticket2 = createticket(request.user,passengers,passengerscount,flight2,flight_2date,flight_2class,coupon,countrycode,email,mobile)

                if(flight_1class == 'Economy'):
                    if f2:
                        fare = (flight1.economy_fare*int(passengerscount))+(flight2.economy_fare*int(passengerscount))
                    else:
                        fare = flight1.economy_fare*int(passengerscount)
                elif (flight_1class == 'Business'):
                    if f2:
                        fare = (flight1.business_fare*int(passengerscount))+(flight2.business_fare*int(passengerscount))
                    else:
                        fare = flight1.business_fare*int(passengerscount)
                elif (flight_1class == 'First'):
                    if f2:
                        fare = (flight1.first_fare*int(passengerscount))+(flight2.first_fare*int(passengerscount))
                    else:
                        fare = flight1.first_fare*int(passengerscount)
            except Exception as e:
                return HttpResponse(e)
            

            if f2:    ##
                return render(request, "flight/payment.html", { ##
                    'fare': fare+FEE,   ##
                    'ticket': ticket1.id,   ##
                    'ticket2': ticket2.id   ##
                })  ##
            return render(request, "flight/payment.html", {
                'fare': fare+FEE,
                'ticket': ticket1.id
            })
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponse("Method must be post.")

def payment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            ticket_id = request.POST['ticket']
            t2 = False
            if request.POST.get('ticket2'):
                ticket2_id = request.POST['ticket2']
                t2 = True
            fare = request.POST.get('fare')
            card_number = request.POST['cardNumber']
            card_holder_name = request.POST['cardHolderName']
            exp_month = request.POST['expMonth']
            exp_year = request.POST['expYear']
            cvv = request.POST['cvv']

            try:
                ticket = Ticket.objects.get(id=ticket_id)
                ticket.status = 'CONFIRMED'
                ticket.booking_date = datetime.now()
                ticket.save()
                if t2:
                    ticket2 = Ticket.objects.get(id=ticket2_id)
                    ticket2.status = 'CONFIRMED'
                    ticket2.save()
                    return render(request, 'flight/payment_process.html', {
                        'ticket1': ticket,
                        'ticket2': ticket2
                    })
                return render(request, 'flight/payment_process.html', {
                    'ticket1': ticket,
                    'ticket2': ""
                })
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be post.")
    else:
        return HttpResponseRedirect(reverse('login'))


def ticket_data(request, ref):
    ticket = Ticket.objects.get(ref_no=ref)
    return JsonResponse({
        'ref': ticket.ref_no,
        'from': ticket.flight.origin.code,
        'to': ticket.flight.destination.code,
        'flight_date': ticket.flight_ddate,
        'status': ticket.status
    })

@csrf_exempt
def get_ticket(request):
    ref = request.GET.get("ref")
    ticket1 = Ticket.objects.get(ref_no=ref)
    data = {
        'ticket1':ticket1,
        'current_year': datetime.now().year
    }
    pdf = render_to_pdf('flight/ticket.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


def bookings(request):
    if request.user.is_authenticated:
        tickets = Ticket.objects.filter(user=request.user).order_by('-booking_date')
        return render(request, 'flight/bookings.html', {
            'page': 'bookings',
            'tickets': tickets
        })
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def cancel_ticket(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            ref = request.POST['ref']
            try:
                ticket = Ticket.objects.get(ref_no=ref)
                if ticket.user == request.user:
                    ticket.status = 'CANCELLED'
                    ticket.save()
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({
                        'success': False,
                        'error': "User unauthorised"
                    })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': e
                })
        else:
            return HttpResponse("User unauthorised")
    else:
        return HttpResponse("Method must be POST.")

def resume_booking(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            ref = request.POST['ref']
            ticket = Ticket.objects.get(ref_no=ref)
            if ticket.user == request.user:
                return render(request, "flight/payment.html", {
                    'fare': ticket.total_fare,
                    'ticket': ticket.id
                })
            else:
                return HttpResponse("User unauthorised")
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponse("Method must be post.")

def contact(request):
    return render(request, 'flight/contact.html')

def privacy_policy(request):
    return render(request, 'flight/privacy-policy.html')

def terms_and_conditions(request):
    return render(request, 'flight/terms.html')

def about_us(request):
    return render(request, 'flight/about.html')

def about_system(request):
    return render(request, 'flight/about_system.html')

def about_devs(request):
    return render(request, 'flight/about_devs.html')
 """