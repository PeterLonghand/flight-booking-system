from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    #path("query/places/<str:q>", views.query, name="query"),
    path("flight", views.flight, name="flight"),
    path("review", views.review, name="review"),
    path("flight/ticket/book", views.book, name="book"),
    path("flight/ticket/payment", views.payment, name="payment"),
    path('flight/ticket/api/<str:ref>', views.ticket_data, name="ticketdata"),
    path('flight/ticket/print',views.get_ticket, name="getticket"),
    path('flight/bookings', views.bookings, name="bookings"),
    path('flight/ticket/cancel', views.cancel_ticket, name="cancelticket"),
    path('flight/ticket/resume', views.resume_booking, name="resumebooking"),
    path('contact', views.contact, name="contact"),
    path('privacy-policy', views.privacy_policy, name="privacypolicy"),
    path('terms-and-conditions', views.terms_and_conditions, name="termsandconditions"),
    path('about-us', views.about_us, name="aboutus"),
    path('about_system', views.about_system, name="about_system"),
    #
    path("query/places/<str:query>/", views.get_places, name="get_places"),
    #
    ##
    path('get-plane-id/<int:flight_id>/', views.get_plane_id, name='get_plane_id'),
    path('get-seat-map/<int:plane_id>/', views.get_seat_map, name='get_seat_map'),
    ##
    path('get-eco-price/<int:flight_id>/', views.get_eco_price, name='get_eco_price'),
    path('get-bus-price/<int:flight_id>/', views.get_bus_price, name='get_bus_price'),

    ###
    path('mark-seat-occupied/', views.mark_seat_occupied, name='mark_seat_occupied'),
    path("mark-seat-available/<str:seat_id>/", views.mark_seat_available, name="mark_seat_available"),

    ###


    path('about_devs', views.about_devs, name="about_devs")
]