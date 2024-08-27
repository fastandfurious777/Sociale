from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Bike, Rental
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from cryptography.fernet import Fernet
from django.conf import settings

@login_required
def home(request):
    user = request.user
    return render(request,"bike_map/map-index.html",context={"user": user})


@login_required
def scanner(request):
    return render(request,"bike_map/scanner.html")

@login_required
def get_bike_positions(request):
    bikes = Bike.objects.filter(is_available=True).values()
    return JsonResponse(
        {"bikes": list(bikes)}
    )

@login_required
@csrf_exempt
def get_bike_code(request):
    if request.method == "GET":
        try:
            bike_id = int(request.GET.get("bike_id"))
            bike = Bike.objects.get(id=bike_id)
            fernet = Fernet(settings.CIPHER_KEY)
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

    
def start_rental(request):
    if request.method == 'POST':
        try:
            user = request.user
            bike_id = json.loads(request.body.decode("utf-8"))
            bike = Bike.objects.get(id=bike_id)
            if not Rental.objects.filter(is_completed=False).filter(user=user):
                Rental(user=user,bike=bike)
                return JsonResponse(
                    {"message" : "Ride successfully started"}, status=200
                )
        except Exception as e:
            return JsonResponse(
                {"message" : f"Unable to start a ride, {e}"}, status=500
            )


def end_rental(request):
    if request.method == "POST":
        try:
            user = request.user
            rental = Rental.objects.get(user=user)
            rental.end_rental()
        except Exception as e:
            return JsonResponse(
                {"message" : f"Unable to end a ride, {e}"}, status=500
            )
        finally:
            return JsonResponse(
                {"message" : f"You successfully finished your ride"}, status=200
            )
"""      
def get_user_status(request):
    user = request.user
    #If there is incompleted rental by user
    active_rental = Rental.objects.filter(is_completed=False).filter(user=user)
    if active_rental:
        context = {
            "rental": active_rental,
            #TODO: Check if needed
            "bike": active_rental.bike
        }
        return render(request,"bike_map/map-index.html",context)
    else:
        return render(request,"bike_map/map-index.html")
 """
