from django.contrib import admin
from django.utils.safestring import mark_safe

from bestflightApp.models import (
    Airline,
    Airplane,
    FlightClass,
    Reservation,
    AvailableFlight,
    AirplaneCapacity,
    AirlineFlightPath,
)


@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active', 'create_date', 'modify_date')
    readonly_fields = ('create_date', 'modify_date', 'is_active')
    search_fields = ['title', 'id']


@admin.register(FlightClass)
class FlightClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'create_date', 'modify_date')
    readonly_fields = ('create_date', 'modify_date',)
    search_fields = ['title', 'id']


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    fields = ('id', 'title', 'create_date', 'modify_date')
    list_display = ('id', 'title', 'capacity', 'create_date', 'modify_date')
    readonly_fields = ('id', 'create_date', 'modify_date',)
    search_fields = ('title', 'id',)

    def capacity(self, obj):
        result = '-'
        airplane_capacities = AirplaneCapacity.objects.filter(airplane=obj.id)
        if airplane_capacities.count():
            result = '<ol style="margin:0; padding-left: 1em">'
            for airplane_capacity in airplane_capacities:
                result += '<li><b style="text-transform: capitalize;">{}</b> - <em>{}<em> </li>'.format( # noqa
                    airplane_capacity.flight_class.title,
                    airplane_capacity.capacity
                )
            result += '</ol>'
            result = mark_safe(result)
        return result


@admin.register(AirplaneCapacity)
class AirplaneCapacityAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'capacity', 'airplane', 'flight_class', 'create_date',
        'modify_date')
    readonly_fields = ('create_date', 'modify_date',)
    search_fields = ['capacity', 'id']


@admin.register(AirlineFlightPath)
class AirlineFlightPathAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'airplane', 'airline', 'pick_up', 'destinaton',
        'should_reoccur', 'reoccurrence_step', 'date_last_flight',
        'create_date', 'modify_date',)
    readonly_fields = ('create_date', 'modify_date', 'date_last_flight')
    search_fields = ['pick_up', 'destinaton', 'id']
    empty_value_display = 'None'


@admin.register(AvailableFlight)
class AvailableFlightAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'airlinePath', 'boarding_time', 'take_off_time',
        'cost', 'no_reversaton', 'create_date', 'modify_date',)
    readonly_fields = ('create_date', 'modify_date', 'no_reversaton')
    search_fields = ['boarding_time', 'take_off_time', 'cost']
    empty_value_display = 'None'


@admin.register(Reservation)
class ReservationFlightAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'flight', 'flight_class', 'user', 'feedback', 'create_date',)
    readonly_fields = ('create_date', 'modify_date',)
    empty_value_display = 'None'
