from django.shortcuts import render,redirect
from .forms import BookingForm

#View function which sends the users booking form with a response back
def create_bookings(request):
    if request.method == "POST":  
        form = BookingForm(request.POST) #binds to the form
        if form.is_valid(): #If the user fills in all the required fields then it is saved
            form.save()
            return redirect('booking_success')
    else:
        form = BookingForm() # empty booking form for the user to film
    return render(request,'booking_form.html',{'form':form}) #connects the python logic to a template, which also sends the form object to the template so it can be displayed

def booking_success(request):
    return render(request,'booking_success.html')