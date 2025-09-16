from django.contrib import admin
from .models import RestaurantSettings, SlotCapacity, Bookings

@admin.register(RestaurantSettings)
class RestaurantSettingsAdmin(admin.ModelAdmin):
    list_display = ('open_time','close_time','slot_minutes','lead_time_minutes')

@admin.register(SlotCapacity)
class SlotCapacityAdmin(admin.ModelAdmin):
    list_display = ('day_of_week','time_of_day','max_bookings')
    list_editable = ('max_bookings',)
    list_filter = ('day_of_week',)
    ordering = ('day_of_week','time_of_day')
@admin.register(Bookings)
class BookingsAdmin(admin.ModelAdmin):
    list_display = ('booking_datetime','name','email','status')
    list_filter = ('status',)
    search_fields = ('name','email','phone_number')
    date_hierarchy = 'booking_datetime'
