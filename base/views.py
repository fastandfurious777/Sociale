from django.shortcuts import render,redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from . forms import CreateUserForm, LoginUserForm, ContactForm, PasswordResetForm
from django.contrib.auth.models import User
from bike_map.models import Bike, Rental
from . import mails
from django.http import HttpResponse


def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = request.POST['name']
            email = request.POST['email']
            message = request.POST['message']
            try:
                mails.contact_confirmation(email)
                mails.contact_inbox(name,email,message)
                messages.success(request, 'All good... We will get back to you shortly!')
            except Exception:
                messages.success(request, 'Something went wrong :( , consider contacting us on IG ')
            return redirect('home')                       
    else:
        context = {
            'form': ContactForm(),
            'available_bikes': Bike.objects.count(),
            'active_users': User.objects.filter(is_active=True).count(),
            #Assuming one rental equals one bus fare (1$)
            'dollars_saved': Rental.objects.count()
        }
        return render(request, 'base/index.html', context)

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CreateUserForm()
    return render(request, 'base/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            #Authentication has been handled by the form
            user = form.get_user()  
            if user is not None:
                login(request, user)  
                return redirect('map-home')  
    else:
        form = LoginUserForm()
    return render(request, 'base/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def password_reset_view(request):
    if request.method == "POST":
        form  = PasswordResetForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(email = request.POST["email"]).first()
            if user is not None:
                return HttpResponse('<h1>Success</h1>')
            #TODO send mail to client with password reset link
            return HttpResponse('<h1>Failuere</h1>')
    else:
        form = PasswordResetForm()
        return render(request, 'base/password-reset.html', {'form': form})