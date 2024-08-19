from django.shortcuts import render

def home(request):
    return render(request,"bike_map/index.html")