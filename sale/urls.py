from django.urls import path
from .views import *

urlpatterns = [
    path("availaibility/<vehicle_id>/<country_code>/", VehicleAvailability.as_view())
]
