from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Vehicle)
admin.site.register(VehicleType)
admin.site.register(VehicleModel)
admin.site.register(VehicleBrand)
admin.site.register(VehiclePrice)
admin.site.register(Currency)