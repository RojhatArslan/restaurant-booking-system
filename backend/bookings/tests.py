from django.test import TestCase
from django.utils import timezone
from datetime import datetime, time as t
from .models import RestaurantSettings, SlotCapacity, Bookings
from .forms import BookingForm

class PerDayCapacityTests(TestCase):
    def setUp(self):
        RestaurantSettings.objects.create(open_time=t(17,0), close_time=t(20,0), slot_minutes=60, lead_time_minutes=0)
        # Wednesday (2): cap 1 at 17:00, Friday (4): cap 2 at 17:00
        SlotCapacity.objects.create(day_of_week=2, time_of_day=t(17,0), max_bookings=1)
        SlotCapacity.objects.create(day_of_week=4, time_of_day=t(17,0), max_bookings=2)

    def aware(self, y,m,d,hh,mm): return timezone.make_aware(datetime(y,m,d,hh,mm))

    def test_wednesday_fills_after_one(self):
        # 2025-01-01 is a Wednesday
        dt = self.aware(2025,1,1,17,0)
        f1 = BookingForm(data={'name':'A','email':'a@x.com','phone_number':'1',
                               'booking_datetime': dt.isoformat(), 'status':'pending'})
        self.assertTrue(f1.is_valid(), f1.errors); f1.save()
        f2 = BookingForm(data={'name':'B','email':'b@x.com','phone_number':'2',
                               'booking_datetime': dt.isoformat(), 'status':'pending'})
        self.assertFalse(f2.is_valid())  # cap is 1 on Wed

    def test_friday_allows_two(self):
        # 2025-01-03 is a Friday
        dt = self.aware(2025,1,3,17,0)
        f1 = BookingForm(data={'name':'A','email':'a@x.com','phone_number':'1',
                               'booking_datetime': dt.isoformat(), 'status':'pending'})
        f2 = BookingForm(data={'name':'B','email':'b@x.com','phone_number':'2',
                               'booking_datetime': dt.isoformat(), 'status':'pending'})
        self.assertTrue(f1.is_valid(), f1.errors); f1.save()
        self.assertTrue(f2.is_valid(), f2.errors); f2.save()
