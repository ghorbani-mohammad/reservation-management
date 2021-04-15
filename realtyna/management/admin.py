from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'created_at',
    )


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('pk', 'bed', 'owner', 'created_at', 'in_reserve')


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'room',
        'reserver',
        'start_date',
        'duration',
        'end_date',
        'created_at',
    )
