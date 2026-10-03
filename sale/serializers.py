from rest_framework import serializers

from vehicle.models import Currency
from .models import *

class VehicleAvailabilityRequestSerializer(serializers.Serializer):
    vehicle_id = serializers.UUIDField()
    country_code = serializers.CharField(max_length=3, min_length=3)

    class Meta:
        fields = ['vehicle_id', 'country_code']

    def validate_country_code(self, value):

        try:
            Currency.objects.get(country_code=value.upper())
            return value
        except:
            raise serializers.ValidationError("Country code provided does not exist in our system")


class BatchItemRequestSerializer(serializers.Serializer):
    vehicle_id = serializers.UUIDField()
    quantity = serializers.IntegerField()
    total_cost_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    unit_price_id = serializers.UUIDField(required=False)

    class Meta:
        fields = '__all__'

    def validate_quantity(self, value):

       if value <= 0:
           raise serializers.ValidationError("Quantity should be at least 1")

       return value
    
    def validate_total_cost_price(self, value):
    
        if value < 1:
            raise serializers.ValidationError("Cost Price should be at least 1")

        return value

    def validate_vehicle_id(self, value):

        try:
            Vehicle.objects.get(id=value)
            return value
        except:
            raise serializers.ValidationError("Vehicle does not exist in our system")


class BatchRequestSerializer(serializers.Serializer):
    purchase_currency_code = serializers.CharField(max_length=3, min_length=3)
    selling_currency_code = serializers.CharField(max_length=3, min_length=3)
    batch_items = BatchItemRequestSerializer(many=True)

    class Meta:
        fields = '__all__'

    def validate_purchase_currency_code(self, value):

        try:
            currency = Currency.objects.get(currency_code=value)
            return currency.id
        except:
            raise serializers.ValidationError("Currency code does not exist")

    def validate_selling_currency_code(self, value):
        try:
            currency = Currency.objects.get(currency_code=value)
            return currency.id
        except:
            raise serializers.ValidationError("Currency code does not exist")


