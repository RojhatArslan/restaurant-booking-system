from django.db import models
# reference  = https://medium.com/django-unleashed/integrating-core-object-oriented-programming-oop-concepts-in-django-powered-music-website-000766b5981f
# Create your models here.
class Customer(models.Model): #models.Model means Customer is a Django model, it matches to a table in the database.
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    phone_number = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"  # How this object shows up in admin or shell


class Table(models.Model):
    number=models.PositiveBigIntegerField(unique=True)
    capacity = models.PositiveBigIntegerField()
    def __str__(self):
        return f"Table{self.number} (Capacity: {self.capacity}) " # How this object shows up in admin or shell
#The str method is a nice way to print the object for easier debugging and admin readability.

class Bookings(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed','Confirmed')
        ('cancelled','Cancelled')

    ]
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)