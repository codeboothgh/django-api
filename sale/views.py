from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from sale.models import BatchItem, Order, OrderItem
from sale.serializers import VehicleAvailabilityRequestSerializer

# Create your views here.

class VehicleAvailability(APIView):

    def get(self, request, **kwargs):

        serializer = VehicleAvailabilityRequestSerializer(data=kwargs)

        serializer.is_valid(raise_exception=True)

        vehicle_id = serializer.validated_data.get("vehicle_id")
        country_code = serializer.validated_data.get("country_code")
        vehicle_batches = BatchItem.objects.filter(
            batch__selling_currency__currency_code=country_code,
            vehicle_id=vehicle_id
        )

        if not vehicle_batches:
            return Response({"detail": "Vehicle is not sold in the selected country"}, status=400)

        total_batch_items_quantities = [vb.quantity for vb in vehicle_batches]

        total_purchased = sum(total_batch_items_quantities)

        total_order_items = OrderItem.objects.filter(
            verhicle_id=vehicle_id,
            order__status="SOLD"
        )

        total_order_items_quantities = [oi.quantity for oi in total_order_items]

        total_sold = sum(total_order_items_quantities)

        stock = total_purchased - total_sold

        return Response (
            {
                "total_batch_items": total_purchased,
                "total_sold": total_sold,
                "in_stock": stock,  
            },
            status=200
        )

# add a view that will return a list of all vehicles and their stock information
# Columns: Vehicle Description, Country Description, Total Batch Items, Total Sold Items, In Stock