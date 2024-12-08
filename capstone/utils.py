from io import BytesIO, StringIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf.files import pisaFileObject


from capstone import settings
#from django.conf.urls.static import static


from flight.models import *
import secrets
from datetime import datetime, timedelta
from xhtml2pdf import pisa

from flight.constant import FEE
import os

""" def link_callback(uri, rel):
    if uri.startswith('file:///'):
        return uri[7:]  # Удаляем 'file://'
    return uri """


""" def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)

# Указываем путь к шрифтам
    font_map = {
        'Roboto-Regular': 'file:///D:/flight-booking-system/flight/Roboto-Regular.ttf'
    }


    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None """

pisaFileObject.getNamedFile = lambda self: self.uri
def fetch_pdf_resources(uri, rel):
    print(uri)
    if uri.find(settings.MEDIA_URL) != -1:
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
    elif uri.find(settings.STATIC_URL) != -1:
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ''))
    else:
        path = None
    #path = path.replace("/", "\\")
    print (path)
    return path

def render_to_pdf(template_src, context_dict={}):
    
    template = get_template(template_src)
    html = template.render(context_dict)
    #html.decode('UTF-8')

    result = BytesIO()
    
    # Обеспечиваем поддержку указанных шрифтов
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result, encoding='utf-8', link_callback=fetch_pdf_resources )
    #pdf = pisa.pisaDocument(StringIO(html.encode("UTF-8")), result, encoding='UTF-8')
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None



def createticket(user,passengers,passengerscount,flight1,flight_1date,flight_1class,coupon,countrycode,email,mobile):
    ticket = Ticket.objects.create()
    ticket.user = user
    ticket.ref_no = secrets.token_hex(3).upper()
    for passenger in passengers:
        ticket.passengers.add(passenger)
    ticket.flight = flight1
    #print(flight_1date)
    ticket.flight_ddate = datetime(int(flight_1date.split('-')[2]),int(flight_1date.split('-')[1]),int(flight_1date.split('-')[0]))
    #print(ticket.flight_ddate)
    ###################
    #print(f'\n\n\n{flight1.depart_datetime}\n\n')
    #flight1ddate = datetime(int(flight_1date.split('-')[2]),int(flight_1date.split('-')[1]),int(flight_1date.split('-')[0]),flight1.depart_time.hour,flight1.depart_time.minute)
    flight1adate = flight1.arrival_datetime
    ###################
    #print('всё ещё ок')
    ticket.flight_adate = datetime(flight1adate.year,flight1adate.month,flight1adate.day)
    #print(ticket.flight_adate)
    
    ffre = 0.0
    if flight_1class.lower() == 'first':
        ticket.flight_fare = flight1.first_fare*int(passengerscount)
        ffre = flight1.first_fare*int(passengerscount)
    elif flight_1class.lower() == 'business':
        ticket.flight_fare = flight1.business_seat_cost*int(passengerscount)
        ffre = flight1.business_seat_cost*int(passengerscount)
    else:
        ticket.flight_fare = flight1.economy_seat_cost*int(passengerscount)
        ffre = flight1.economy_seat_cost*int(passengerscount)
    ticket.other_charges = FEE
    if coupon:
        ticket.coupon_used = coupon                     ##########Coupon
    ticket.total_fare = ffre+FEE+0.0                    ##########Total(Including coupon)
    ticket.seat_class = flight_1class.lower()
    #TODO: сделать так, чтобы у каждого пассажира был свой класс обслуживания
    ticket.status = 'PENDING'
    ticket.mobile = ('+'+countrycode+' '+mobile)
    ticket.email = email
    ticket.save()
    #print(ticket.user)
    print(ticket)
    return ticket