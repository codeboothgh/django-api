from rest_framework import serializers

from vehicle.models import Vehicle, VehicleType,VehicleModel,VehicleBrand,VehiclePrice,Currency

class VehicleTypeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = VehicleType
        read_only_fields = ["id", "created_by", "created_at", "slug"]

    # i want to customize what happen when a new bject is created
    def create(self, validated_data):
        instance = super().create(validated_data)

        name = validated_data.get("name")
        instance.slug = name.replace(" ", "-").lower()

        instance.save()
        
        return instance

#Vehicle Model Serializer
class VehicleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleModel
        fields = "__all__" # include all fields including the one inf=herited from the AbstractField
        read_only_fields = [ # the user is not allow to change this fields, it meant to be read only
            "id",
            "slug",
            "created_at",
            "created_by",
        ]

        #since the vehiclemodel has a name which is required we should validate them
        def validate_name(self, value):
            if not value.strip():
                raise serializers.ValidationError("Vehicle model cannot be empty")
            return value

# Vehicle Brand
class VehicleBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleBrand
        fields = "__all__"
        read_only_fields = [
            "id",
            "slug",
            "created_at",
            "created_by",
        ]     

        def validate_name(self, value):
            if not value.strip():
                raise serializers.ValidationError("Vehicle brand can not be empty")
            return value

# Vehicle Price      
class VehiclePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehiclePrice  
        fields = "__all__"
        read_only_fields = [
            "id",
            "slug",
            "created_at",
            "created_by",
        ]

        def validate_price(self, value):
            if value <= 0 :
                raise serializers.ValidationError("Vehicle Price  must be greater than zero")
            return value

#Currency for the prices
class CurrencySerializer(serializers.ModelSerializer):
    class Meta :
        model = Currency
        fields = "__all__"
        read_only_fields = [
            "id",
            "slug",
            "created_at",
            "created_by",
        ]

        def validate_short_name(self,value):
            #so the model can stop null so we need check if null we return the empty
            #then most of the country currency shortname is more than one letter, so we check that
            if value is None:
                return value

            if len(value.strip()) < 2:
                raise serializers.ValidationError("Short name must conatin at least two characters")
            return value

class VehicleRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = [
            "vehicle_model",
            "vehicle_type",
            "brand",
            "color",
            "chassis",
            "mileage",
            "year"
        ]

    def validate_year(self, value):
        import re

        pattern = r"^[1-3][0-9]{3}$"

        match = re.search(pattern, str(value))
        print(match)
        if match:
            return value

        raise serializers.ValidationError("Year format invalid")