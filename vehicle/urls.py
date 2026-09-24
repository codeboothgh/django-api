from django.urls import path

from vehicle.views import *

urlpatterns = [
    path("type/create/", CreateVehicleType.as_view()),
    path("model/create/", CreateVehicleModel.as_view()),
    path("brand/create/", CreateVehicleBrand.as_view()),
    path("price/create/", CreateVehiclePrice.as_view()),
    path("create/", CreateVehicle.as_view()),
    path("currency/create/", CreateCurrency.as_view()),

    #======================LISAPIView URL ================================
    path("vehicle-model/list/", ListVehicleModel.as_view()),
    path("vehicle-price/list/", ListVehiclePrice.as_view()),
    path("vehicle-brand/list/", ListVehicleBrand.as_view()),
    path("currency/list/", ListCurrency.as_view()),
    path("vehicle-type/list/", ListVehicleType.as_view()),
]
