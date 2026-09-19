from rest_framework.generics import CreateAPIView,ListAPIView

from vehicle.models import VehicleType,VehicleModel,VehicleBrand,VehiclePrice,Currency
from vehicle.serializers import VehicleTypeSerializer,VehicleModelSerializer,VehicleBrandSerializer,VehiclePriceSerializer,CurrencySerializer

class CreateVehicleType(CreateAPIView):
    serializer_class = VehicleTypeSerializer


#The Vehicle Model View
# for create there is no object to find, the client is just sendind the data ,so we dont need queryset=()
# also serailezer can tell django what model to create when serailize.save() is called by VehicleModelSerializer
class CreateVehicleModel(CreateAPIView):
    serializer_class = VehicleModelSerializer  

#Vehicle brand view
class CreateVehicleBrand(CreateAPIView):
    serializer_class = VehicleBrandSerializer    
    

#Vehicle Price View 
class CreateVehiclePrice(CreateAPIView):
    serializer_class = VehiclePriceSerializer  

# Currency for the Prices
class CreateCurrency(CreateAPIView):
    serializer_class = CurrencySerializer     

# ================================================== ListAPIViews=========================================
class ListVehicleModel(ListAPIView):
    queryset = VehicleModel.objects.all() # get all the existing vehiclemodel record
    serializer_class = VehicleModelSerializer # and use the srializer to comvert it into somethimg DRF can work with which is Json


#Vehicle brand lsit
class ListVehicleBrand(ListAPIView):
    queryset = VehicleBrand.objects.all() 
    serializer_class = VehicleBrandSerializer


#Vehicle price list
class ListVehiclePrice(ListAPIView):
    queryset = VehiclePrice.objects.all()
    serializer_class = VehiclePriceSerializer  

# currency price list
class ListCurrency(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer  

#Vehicle type
class ListVehicleType(ListAPIView):
    queryset = VehicleType.objects.all()  
    serializer_class = VehicleTypeSerializer     


