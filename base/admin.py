from django.contrib import admin
from . models import Bike, Rental


# Register your models here.


class BikeAdmin(admin.ModelAdmin):
    model = Bike
    list_display = ["name","lat","lon","is_available","last_taken_by","last_updated"]
class RentalAdmin(admin.ModelAdmin):
    model = Rental
    list_display = ["user","bike","started_at","finished_at"]

admin.site.register(Bike,BikeAdmin)
admin.site.register(Rental,RentalAdmin)