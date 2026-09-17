from rest_framework import serializers

from vehicle.models import VehicleType

class VehicleTypeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = VehicleType
        read_only_fields = ["id", "created_by", "created_at", "slug"]

    def create(self, validated_data):
        instance = super().create(validated_data)

        name = validated_data.get("name")
        instance.slug = name.replace(" ", "-").lower()

        instance.save()
        
        return instance