
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.views import APIView
from bike_map.selectors import parking_list, parking_get
from bike_map.services import parking_create, parking_update, parking_delete

class ParkingListApi(APIView):
    raise NotImplementedError
    
class ParkingDetailApi(APIView):
    pass
        
class ParkingUpdateApi(APIView):
   pass

class ParkingDeleteApi(APIView):
    pass
