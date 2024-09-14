from . models import Parking

def valid_location(coords):
    parkings = Parking.objects.all()
    for parking in parkings:
        if parking.contains_point(coords):
            return True
    return False