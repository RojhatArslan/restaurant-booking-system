from datetime import datetime, timedelta

from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from .models import RestaurantSettings, SlotCapacity, DAYS
from .forms import WeeklyCapacitySetupForm

def _generate_slot_times(open_time, close_time, slot_minutes):
    """Yield time objects for each slot between open (inclusive) and close (exclusive)."""
    # Use a dummy date to build datetimes, then take .time()
    base = datetime(2000,1,1, open_time.hour, open_time.minute)
    end  = datetime(2000,1,1, close_time.hour, close_time.minute)
    step = timedelta(minutes=slot_minutes)
    cur = base
    while cur < end:
        yield cur.time()
        cur += step

def setup_weekly_capacity(request):
    """
    Simple owner page: set per-day default capacity.
    Creates/updates SlotCapacity for every slot (Mon–Sun), respecting open/close and slot size.
    """
    settings = RestaurantSettings.objects.first()
    if not settings:
        messages.error(request, "Please create RestaurantSettings in Admin first.")
        return redirect('home')

    if request.method == "POST":
        form = WeeklyCapacitySetupForm(request.POST)
        if form.is_valid():
            mon_thu = form.cleaned_data['mon_thu_capacity']
            fri = form.cleaned_data['fri_capacity']
            sat = form.cleaned_data['sat_capacity']
            sun = form.cleaned_data['sun_capacity']
            overwrite = form.cleaned_data['overwrite']

            caps_by_day = {
                0: mon_thu, 1: mon_thu, 2: mon_thu, 3: mon_thu,  # Mon–Thu
                4: fri, 5: sat, 6: sun,                          # Fri, Sat, Sun
            }

            created, updated = 0, 0
            for dow in range(7):
                for slot_time in _generate_slot_times(settings.open_time, settings.close_time, settings.slot_minutes):
                    obj, exists = SlotCapacity.objects.get_or_create(
                        day_of_week=dow,
                        time_of_day=slot_time,
                        defaults={'max_bookings': caps_by_day[dow]}
                    )
                    if exists:
                        created += 1
                    else:
                        if overwrite:
                            if obj.max_bookings != caps_by_day[dow]:
                                obj.max_bookings = caps_by_day[dow]
                                obj.save(update_fields=['max_bookings'])
                                updated += 1

            messages.success(request, f"Weekly capacities created: {created}, updated: {updated}.")
            return redirect('setup_weekly_capacity')
    else:
        form = WeeklyCapacitySetupForm()

    return render(request, 'setup_weekly_capacity.html', {'form': form, 'settings': settings, 'days': DAYS})
