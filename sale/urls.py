from django.urls import path
from .views import *

urlpatterns = [
    path("batch/create/", CreateBatch.as_view()),
    path("availaibility/<vehicle_id>/<country_code>/", VehicleAvailability.as_view())
]
