from django.db import models
# reference  = https://medium.com/django-unleashed/integrating-core-object-oriented-programming-oop-concepts-in-django-powered-music-website-000766b5981f
# Create your models here.

# i USED Django Django’s ORM (Object-Relational Mapping, which allows python objects to work with sql instead of writing raw sql
class Customer(models.Model): #models.Model means Customer is a Django model, it matches to a table in the database.
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    phone_number = models.CharField(max_length=50)

    def __str__(self): # returns a string representing an object.
        return f"{self.first_name} {self.last_name}"  # How this object shows up in admin or shell


class Table(models.Model):
    number=models.PositiveBigIntegerField(unique=True)
    capacity = models.PositiveBigIntegerField()
    def __str__(self): # returns a string representing an object.
        return f"Table{self.number} (Capacity: {self.capacity}) " # refers to the table field on Booking


class Bookings(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed','Confirmed'),
        ('cancelled','Cancelled'),

    ]
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE) # customer is a foreign key to Customer object
    table = models.ForeignKey(Table,on_delete=models.CASCADE) #if the Customer or Table is deleted  the Booking will also be deleted automatically.
    booking_datetime=models.DateTimeField()
    party_size=models.PositiveIntegerField()
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='pending')

    def __str__(self):
        return f"Booking for {self.customer} at {self.booking_datetime} on {self.table}" #calls the str method on the related customer which shows booking date and time, and table assigned
