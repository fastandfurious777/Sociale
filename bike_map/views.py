from django.shortcuts import render
from .models import Bike
from django.http import JsonResponse
def home(request):
    bikes = Bike.objects.filter(is_available=True).values()
    return render(request,"bike_map/index.html",context = {"bikes": list(bikes)})

def bike_positions(request):
    bikes = Bike.objects.filter(is_available=True).values()
    return JsonResponse(
        {"bikes": list(bikes)}
    )