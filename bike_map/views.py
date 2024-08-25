from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Bike, Rental
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@login_required
def home(request):
    bikes = Bike.objects.filter(is_available=True).values()
    return render(request,"bike_map/index.html",context = {"bikes": list(bikes)})
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
            bike_id = int(request.GET.get("qr_code"))
            bike = Bike.objects.get(id=bike_id)
        except ValueError:
            return JsonResponse({"message": "Wrong QR code provided"}, status = 400)
        except Exception:
            return JsonResponse({"message": "Some unexpected error ocured"}, status= 500)
        finally:
            return JsonResponse(
                {"message": "Code successfully scanned", "bike_code": bike.encrypted_code}, status=200

            )

    
def start_rental(request):
    if request.method == 'POST':
        try:
            user = request.user
            bike_id = json.loads(request.body.decode("utf-8"))
            #If User has no rentals at that time
            if not Rental.objects.filter(is_completed=False).filter(user=user):
                Rental(user=user,bike=Bike.objects.get(id=bike_id))
                pass
        except Exception as e:
            return JsonResponse(
                {"message" : f"Unable to end a ride, {e}"}, status=500
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

