from rest_framework.generics import CreateAPIView

from vehicle.models import VehicleType
from vehicle.serializers import VehicleTypeSerializer

class CreateVehicleType(CreateAPIView):
    serializer_class = VehicleTypeSerializer