from django.db import models
from django.utils import timezone
from datetime import time as t

DAYS = [
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
]

class RestaurantSettings(models.Model):
    open_time = models.TimeField(default=t(10, 0))     # inclusive
    close_time = models.TimeField(default=t(22, 0))    # exclusive
    slot_minutes = models.PositiveIntegerField(default=60)
    lead_time_minutes = models.PositiveIntegerField(default=30)
    def __str__(self):
        return f"Settings {self.open_time}-{self.close_time} / {self.slot_minutes}m"

class SlotCapacity(models.Model):
    day_of_week = models.PositiveSmallIntegerField(choices=DAYS)  # 0=Mon ... 6=Sun
    time_of_day = models.TimeField(help_text="e.g. 17:00")
    max_bookings = models.PositiveIntegerField(default=30)

    class Meta:
        unique_together = ('day_of_week', 'time_of_day')
        ordering = ('day_of_week', 'time_of_day')

    def __str__(self):
        return f"{self.get_day_of_week_display()} {self.time_of_day} ⇒ {self.max_bookings}"



class Bookings(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)          # temporarily nullable
    email = models.EmailField(blank=True, null=True)                        # already nullable
    phone_number = models.CharField(max_length=50, blank=True, null=True)   # temporarily nullable
    booking_datetime = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS, default='pending')

    class Meta:
        ordering = ['booking_datetime']
        indexes = [models.Index(fields=['booking_datetime'])]

    def __str__(self):
        return f"{self.name} @ {self.booking_datetime} ({self.status})"

    @staticmethod
    def slot_start(dt, slot_minutes:int):
        return dt.replace(minute=(dt.minute // slot_minutes) * slot_minutes, second=0, microsecond=0)
