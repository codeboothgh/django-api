from rest_framework import serializers

from vehicle.models import Currency

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
