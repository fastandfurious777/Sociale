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
                try:
                    mails.password_reset(user.email,reset.uuid)
                except:
                    return HttpResponse("<p>We have encountered a server error, report a bug on @Sociale.x</p>")
                return HttpResponse("<p>All good, check your email</p>")
            else:
                return HttpResponse("<p>Your account doesnt exist... </p>") 
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
        


import json
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . utils import valid_location
from . models import Bike, Rental, Parking

#@login_required
def home(request): 
    user = request.user
    return render(request, "bike_map/map-index.html", context={"user": user, "api_key": settings.MAPS_KEY})

@login_required
def scanner(request):
    return render(request,"bike_map/scanner.html")

def get_user_status(request):
    user = request.user
    try:
        #If there is incompleted rental by user
        active_rental = Rental.objects.filter(is_completed=False).filter(user=user)
        if active_rental:
            return JsonResponse(
                {"active_rental": True},status=200
            )
        else:
            return JsonResponse(
                {"active_rental": False},status=200
            )
    except Exception as e:
        return JsonResponse(
                {"message": f"{e}, ocured"},status=400
            )



@login_required
@csrf_exempt
def get_bike_code(request):
    if request.method == "GET":
        try:
            user = request.user
            bike_id = int(request.GET.get("bike_id"))
            bike = Bike.objects.get(id=bike_id)
            # fernet = Fernet(settings.CIPHER_KEY)
            bike_code = bike.code 
            '''fernet.decrypt(bike.code).decode()'''
        except ValueError:
            return JsonResponse({"message": "Wrong QR code provided"}, status = 400)
        except Exception:
            return JsonResponse({"message": "Some unexpected error ocured"}, status= 500)
        finally:
            return JsonResponse(
                {"message": "Code successfully scanned", "bike_code": bike_code}, status=200

            )

@csrf_exempt
def start_rental(request):
    if request.method == 'POST':
        try:
            user = request.user 
            data = json.loads(request.body.decode('utf-8'))
            bike = Bike.objects.get(id=data['bike_id'])
            if not Rental.objects.filter(is_completed=False).filter(user=user):
                rental = Rental(user=user,bike=bike)
                rental.start_rental()
                return JsonResponse(
                    {"message" : "Ride successfully started"}, status=200
                )
        except Exception as e:
            return JsonResponse(
                {"message" : f"Unable to start a ride, {e}"}, status=500
            )

@csrf_exempt
def end_rental(request):
    if request.method == "POST":
        try:
            user = request.user
            data = json.loads(request.body.decode('utf-8'))
            coords = (data['lat'],data['lon'])
            
            rental = Rental.objects.filter(is_completed=False).filter(user=user).first()
            if valid_location(coords):
                rental.end_rental(data['lat'],data['lon'])
                return JsonResponse(
                {"message" : f"You successfully finished your ride"}, status=200
            )
            else:
                return JsonResponse(
                {"message" : f"Can't end your ride here"}, status=400
                )
        except Exception as e:
            print("its valid")
            return JsonResponse(
                {"message" : f"Unable to end a ride, {e}"}, status=500
            )
            
# CLEANING UPP, heres utils.py
from . models import Parking

#TODO
def valid_location(coords):
    parkings = Parking.objects.all()
    for parking in parkings:
        if parking.contains_point(coords):
            return True
    return False

#CODE on QRS
#ENCRYPT <- think about it ???
#DECRYPT <- think about it ???




    