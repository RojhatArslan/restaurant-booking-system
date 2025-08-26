from django import forms
from .models import Bookings  #import the database structure


class BookingForm(forms.ModelForm):
    class Meta:
        model = Bookings
        fields = ['customer','table','booking_datetime','party_size','status']
