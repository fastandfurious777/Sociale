from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Bike, Rental, Parking
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from . utils import valid_location

# from cryptography.fernet import Fernet
# from django.conf import settings

@login_required
def home(request):
    user = request.user
    return render(request, "bike_map/map-index.html", context={"user": user})

@login_required
def scanner(request):
    return render(request,"bike_map/scanner.html")

#@login_required
def bike_list(request):
    if request.method == 'GET':
        active_param = request.GET.get('active', None)
        if active_param is not None:
            if active_param.lower() in ['true','yes','1']:
                bikes = Bike.objects.filter(is_available=True).values()
            elif active_param.lower() in ['false','no','0']:
                bikes = Bike.objects.filter(is_available=True).values()
            else:
                return JsonResponse(
                    {"error": "Invalid 'active' parameter"}, status=400
                )
        else:
            bikes = Bike.objects.all().values()
        return JsonResponse(
            {"bikes": list(bikes)}, status=200
        )
    else:
        return JsonResponse(
            {"error": "Bad request"}, status=400
        )
    
def bike_management(request, id):
    if request.method == 'GET':
        bike = Bike.objects.filter(id=id).first()
        if bike is not None:
            return JsonResponse(
                {
                    'id': bike.id,
                    'name': bike.name,
                    'is_available': bike.is_available
                }, status = 200
            )
        else:
            return JsonResponse(
                {"error": "Not found"}, status = 404
            )
    #TODO    
    elif request.method == 'POST':
        # Create bike 
        pass
    elif request.method == 'PUT':
        # Update bikes properties
        pass
    elif request.method == 'DELETE':
        # Update bikes properties
        pass

def polygon_list(request):
    if request.method == 'GET':
        parkings = Parking.objects.all()
        response = []
        for parking in parkings:
            response.append(
                {
                    "name": parking.name,
                    "coords": [{"lat":coord[0],"lng":coord[1]} for coord in parking.coords]
                }
            )
        return JsonResponse(
            {"polygons": list(response)}, status=200
        )
def polygon_management(request,id):
    pass

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
            
   

