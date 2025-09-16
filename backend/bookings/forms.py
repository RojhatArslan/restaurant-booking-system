from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Bookings, RestaurantSettings, SlotCapacity

class BookingForm(forms.ModelForm):
    """Basic capacity-per-slot validation."""
    class Meta:
        model = Bookings
        fields = ['name','email','phone_number','booking_datetime','status']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control'}),
            'booking_datetime': forms.DateTimeInput(attrs={'type':'datetime-local','class':'form-control'}),
            'status': forms.Select(attrs={'class':'form-select'}),
        }

    def clean(self):
        cleaned = super().clean()
        dt = cleaned.get('booking_datetime')
        if not dt:
            return cleaned

        s = RestaurantSettings.objects.first()
        if not s:
            # minimal defaults so you don't crash in dev
            from datetime import time as t
            class S: pass
            s = S(); s.open_time=t(12,0); s.close_time=t(22,0); s.slot_minutes=60; s.lead_time_minutes=30

        local_dt = timezone.localtime(dt) if timezone.is_aware(dt) else dt

        # Rule 1: lead time + hours
        if local_dt < timezone.localtime(timezone.now()) + timedelta(minutes=s.lead_time_minutes):
            self.add_error('booking_datetime', f'Must be at least {s.lead_time_minutes} minutes in advance.')
        if not (s.open_time <= local_dt.time() < s.close_time):
            self.add_error('booking_datetime', f'Outside opening hours ({s.open_time}–{s.close_time}).')

        # Rule 2: align to slot start
        slot = Bookings.slot_start(local_dt, s.slot_minutes)
        if local_dt != slot:
            self.add_error('booking_datetime', f'Use slot boundaries (every {s.slot_minutes} minutes).')

        # Rule 3: capacity check for that slot time_of_day
        cap = SlotCapacity.objects.filter(time_of_day=slot.time()).first()
        if not cap:
            self.add_error('booking_datetime', 'No capacity configured for this slot.')
        else:
            count = Bookings.objects.filter(
                booking_datetime__date=slot.date(),
                booking_datetime__time=slot.time(),
            ).exclude(pk=self.instance.pk if self.instance and self.instance.pk else None).count()
            if count >= cap.max_bookings:
                self.add_error('booking_datetime', f'Slot full at {slot.time()}.')

        return cleaned
