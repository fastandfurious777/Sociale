from django.shortcuts import render,redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from . forms import CreateUserForm, LoginUserForm, ContactForm,RequestResetForm, PasswordResetForm

from django.contrib.auth.models import User
from bike_map.models import Bike, Rental
from . models import ResetPassword
from . import mails

from django.utils import timezone
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
        form  = RequestResetForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(email = request.POST["email"]).first()
            if user is not None:
                reset = ResetPassword.objects.filter(user=user).first()
                if not reset:
                    reset = ResetPassword()
                    reset.set_uuid(user=user)
                else:
                    reset.set_uuid(user=user)
                mails.password_reset(user.email,reset.uuid)
                return HttpResponse("<p>All good, check your email</p>") 
            return HttpResponse("<p>Something went wrong... </p>") 
    else:
        form = RequestResetForm()
        return render(request, 'base/request-reset.html', {'form': form})

def verify_reset_view(request,uuid):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            try:
                reset = ResetPassword.objects.get(uuid=uuid)
                new_password = request.POST['password1']
                user = reset.user
                #Delete used token
                reset.delete()
                user.set_password(new_password)
                user.save()       
                return HttpResponse("<p>Your password was set successfully, <a href = '/login/'>Login</a></p>")
            except:
                return HttpResponse("<p>Something went wrong, <a href = '/' Contact Us</a></p>")
        else:
            return render(request, 'base/password-reset.html', {'form': form})
    else:
        reset = ResetPassword.objects.filter(uuid = uuid).first()
        print(reset)
        if reset is None: 
            return HttpResponse("<p>Wrong token, generate a <a href ='/password-reset/'>new one</a></p>")
        elif reset.last_updated < timezone.now() - timezone.timedelta(hours=1):
            return HttpResponse("<p>Your token has expired, generate a <a href ='/password-reset/'>new one</a></p>")
        else:
            form = PasswordResetForm()
            return render(request, 'base/password-reset.html', {'form': form})


    