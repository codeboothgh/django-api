from rest_framework import serializers

from vehicle.models import Vehicle, VehicleType,VehicleModel,VehicleBrand,VehiclePrice,Currency


READ_ONLY_FIELDS = ["id", "created_by", "created_at", "slug"]
class VehicleTypeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = VehicleType
        read_only_fields = READ_ONLY_FIELDS

    # i want to customize what happen when a new object is created
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
        read_only_fields = READ_ONLY_FIELDS

    #since the vehiclemodel has a name which is required we should validate them
    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Vehicle model cannot be empty")
        return value

    # slugify the name of the brand
    def create(self, validated_data):
        instance = super().create(validated_data)

        name = validated_data.get("name")
        instance.slug = name.replace(" ", "-").lower()
        request = self.context.get("request", None)
        if not request:
            return instance

        instance.created_by = request.user
        instance.save()

        return instance

# Vehicle Brand
class VehicleBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleBrand
        fields = "__all__"
        read_only_fields = READ_ONLY_FIELDS

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Vehicle brand can not be empty")
        return value

    # slugify the name of the brand
    def create(self, validated_data):
        instance = super().create(validated_data)

        name = validated_data.get("name")
        instance.slug = name.replace(" ", "-").lower()
        request = self.context.get("request", None)
        if not request:
            return instance
        
        instance.created_by = request.user
        instance.save()
        
        return instance


# Vehicle Price      
class VehiclePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehiclePrice  
        fields = "__all__"
        read_only_fields = READ_ONLY_FIELDS

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

    def validate_currency_code(self,value):
        #so the model can stop null so we need check if null we return the empty
        #then most of the country currency shortname is more than one letter, so we check that
        if value is None:
            return value

        if len(value.strip()) < 2:
            raise serializers.ValidationError("Currency code must conatin at least two characters")
        return value

    def create(self, validated_data):
        instance = super().create(validated_data)
        # save who creates the currency with request from context
        request = self.context.get("request", None)
        if not request:
            return instance

        instance.created_by = request.user
        instance.save()

        return instance


class VehicleRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = [
            "vehicle_model",
            "vehicle_type",
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

    def validate_color(self, value):
        return value.capitalize()

    
class VehicleResponseSerializer(serializers.ModelSerializer):
    vehicle_model = VehicleModelSerializer(many=False)
    vehicle_type = VehicleTypeSerializer(many=False)

    class Meta:
        fields = '__all__'
        read_only_fields = READ_ONLY_FIELDS
        model = Vehicle