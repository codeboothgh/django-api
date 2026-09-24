from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework.permissions import IsAuthenticated
from user.permissions import AdminPermission, ManagerPermission
from vehicle.models import VehicleType,VehicleModel,VehicleBrand,VehiclePrice,Currency
from vehicle.serializers import VehicleResponseSerializer, VehicleRequestSerializer, VehicleTypeSerializer,VehicleModelSerializer,VehicleBrandSerializer,VehiclePriceSerializer,CurrencySerializer
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


class CreateVehicleType(CreateAPIView):
    permission_classes = [AdminPermission,]
    serializer_class = VehicleTypeSerializer


#The Vehicle Model View
# for create there is no object to find, the client is just sendind the data ,so we dont need queryset=()
# also serailezer can tell django what model to create when serailize.save() is called by VehicleModelSerializer
class CreateVehicleModel(CreateAPIView):
    permission_classes = [AdminPermission,]
    serializer_class = VehicleModelSerializer  

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context  

#Vehicle brand view
class CreateVehicleBrand(CreateAPIView):
    permission_classes = [AdminPermission,]
    serializer_class = VehicleBrandSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context    
    

#Vehicle Price View 
class CreateVehiclePrice(CreateAPIView):
    permission_classes = [AdminPermission,]
    serializer_class = VehiclePriceSerializer  

# Currency for the Prices
class CreateCurrency(CreateAPIView):
    permission_classes = [AdminPermission,]
    serializer_class = CurrencySerializer

    # add request to the serializer's context
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context



# ================================================== ListAPIViews=========================================
class ListVehicleModel(ListAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = VehicleModel.objects.all() # get all the existing vehiclemodel record
    serializer_class = VehicleModelSerializer # and use the srializer to comvert it into somethimg DRF can work with which is Json


#Vehicle brand lsit
class ListVehicleBrand(ListAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = VehicleBrand.objects.all() 
    serializer_class = VehicleBrandSerializer


#Vehicle price list
class ListVehiclePrice(ListAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = VehiclePrice.objects.all()
    serializer_class = VehiclePriceSerializer  

# currency price list
class ListCurrency(ListAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer  

#Vehicle type
class ListVehicleType(ListAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = VehicleType.objects.all()  
    serializer_class = VehicleTypeSerializer     


class CreateVehicle(CreateAPIView):
    permission_classes = [ManagerPermission,]
    serializer_class = VehicleRequestSerializer

    def create(self, request):
        input_serializer = self.get_serializer(data=request.data)

        input_serializer.is_valid(raise_exception=True)

        vehicle = input_serializer.save()

        vehicle.created_by = self.request.user
        vehicle.slug = f"{vehicle.vehicle_model.brand.name}-{vehicle.vehicle_model.name}-{vehicle.color}-{vehicle.year}".lower()
        vehicle.save()

        serializer = VehicleResponseSerializer(vehicle, context=self.get_serializer_context())

        return Response(
            serializer.data,
            status=201
        )