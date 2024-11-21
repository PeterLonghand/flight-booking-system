""" from django.contrib import admin

from .models import * """

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Place, Flight, Passenger, Ticket, TransportCompany, PlaneModel, Plane, SeatClass, Seat

from django import forms

# Создаем кастомный админ-класс для пользователя
class UserAdmin(BaseUserAdmin):
    # Используем только ваши кастомные поля
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('firstname', 'surname', 'patronymic', 'phonenumber', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'firstname', 'surname', 'email', 'is_staff', 'is_active'),
        }),
    )
    list_display = ('username', 'email', 'firstname', 'surname', 'is_staff')
    search_fields = ('username', 'email', 'firstname', 'surname')
    ordering = ('username',)

# Регистрируем кастомную модель пользователя с кастомным админ-классом
admin.site.register(User, UserAdmin)
admin.site.register(Place)
""" admin.site.register(Week) """
admin.site.register(Flight)
admin.site.register(Passenger)
admin.site.register(Ticket)
admin.site.register(TransportCompany)
admin.site.register(PlaneModel)
admin.site.register(Plane)
admin.site.register(SeatClass)
admin.site.register(Seat)



""" 
admin.site.register(Place)
admin.site.register(Week)
admin.site.register(Flight)
admin.site.register(Passenger)
admin.site.register(User)
admin.site.register(Ticket) """