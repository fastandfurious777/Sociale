import factory
import json
from parkings.models import Parking

def create_coords(coords: list[list[int, int]]) -> str:
    """"Creates simple coords for testing purposes"""
    area = {
        "type": "Polygon",
        "coordinates": [ coords ]
    }
    return json.dumps(area)
class TestParkingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Parking
    
    class Params:
        coords = [[0, 0], [0, 3], [3, 3], [3, 0], [0, 0]]
    
    # Workaround for unique name as factory didn't implement such, more info:
    # https://github.com/FactoryBoy/factory_boy/issues/305
    name = factory.Sequence(lambda n: f"Parking{n}")
    area = factory.LazyAttribute(lambda o: create_coords(o.coords))
    is_active = True
