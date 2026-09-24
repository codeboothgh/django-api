from django.db import models

from user.models import AbstractFields

# Create your models here.

class Vehicle(AbstractFields):
    vehicle_type = models.ForeignKey(
        "VehicleType",
        related_name="vehicle_vehicle_type",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    vehicle_model = models.ForeignKey(
        "VehicleModel",
        related_name="vehicle_vehicle_model",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    color = models.CharField(max_length=255, blank=True, null=True)
    mileage = models.PositiveIntegerField(blank=True, null=True, db_default=0)
    year = models.IntegerField(blank=True, null=True)
    chassis = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "vehicle"
        permissions = (
            ('can_read', 'Can read vehicle information'),
            ('can_write', 'Can create, update or delete vehicle.')
        )

    def __str__(self):
        return f"({self.vehicle_type}) - {self.vehicle_model} {self.year}"


class VehicleType(AbstractFields):
    name = models.CharField(max_length=255)
    wheels =  models.IntegerField(blank=True, null=True, db_default=2)
    description =  models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "vehicle_type"

    def __str__(self):
        return self.name


class VehicleModel(AbstractFields):
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(
        "VehicleBrand",
        related_name="model_brand",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        db_table = "vehicle_model"

    def __str__(self):
        return self.brand.name + " " + self.name


class VehicleBrand(AbstractFields):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = "vehicle_brand"

    def __str__(self):
        return self.name


TYPE = [
    ("SELLING", "Selling Price"),
    ("COST", "Cost Price")
]
class VehiclePrice(AbstractFields):
    price_type = models.CharField(choices=TYPE, max_length=10)
    vehicle = models.ForeignKey(
        Vehicle,
        related_name="vehicle_vehicle_price",
        on_delete=models.CASCADE
    )
    price = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.ForeignKey(
        "Currency",
        related_name="currency_vehicle_price",
        on_delete=models.SET_NULL,
        blank=True, null=True
    )

    class Meta:
        db_table = "vehicle_price"

    def __str__(self):
        return f"{self.vehicle}, {self.currency} {self.price}"


class Currency(AbstractFields):
    sign = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    currency_code = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    country_code = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "currency"

    def __str__(self):
        return self.currency_code