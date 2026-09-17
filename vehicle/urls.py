from django.urls import path

from vehicle.views import CreateVehicleType

urlpatterns = [
    path("vehicle-type/create/", CreateVehicleType.as_view())
]
