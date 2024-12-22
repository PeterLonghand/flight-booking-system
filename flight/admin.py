""" from django.contrib import admin

from .models import * """


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Place, Flight, Passenger, Ticket, TransportCompany, PlaneModel, Plane, SeatClass, Seat

from django import forms

# Создаем кастомный админ-класс для пользователя
class UserAdmin(BaseUserAdmin):
    # Используем только свои кастомные поля
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

@admin.register(PlaneModel)
class PlaneModelAdmin(admin.ModelAdmin):    
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

# Регистрируем кастомную модель пользователя с кастомным админ-классом
#admin.site.register(User, UserAdmin)
admin.site.register(Place)
""" admin.site.register(Week) """
admin.site.register(Flight)
#admin.site.register(Passenger)
#admin.site.register(Ticket)
admin.site.register(TransportCompany)
#admin.site.register(PlaneModel)
admin.site.register(Plane)
#admin.site.register(SeatClass)
#admin.site.register(Seat)
