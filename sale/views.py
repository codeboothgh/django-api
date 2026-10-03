from django.db import transaction
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from sale.models import Batch, BatchItem, OrderItem
from sale.serializers import VehicleAvailabilityRequestSerializer, BatchRequestSerializer
from user.permissions import ManagerPermission
from utils.codes import new_batch_number
from vehicle.models import Currency

# Create your views here.
class CreateBatch(CreateAPIView):
    permission_classes = [ManagerPermission,]
    serializer_class = BatchRequestSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        serializer = BatchRequestSerializer(data=self.request.data)

        serializer.is_valid(raise_exception=True)

        # batch_number = ddmmyyhhmm001
        previous_batch = None
        try:
           previous_batch = Batch.objects.first()
        except:
            pass

        batch_number = new_batch_number(previous_batch.batch_number if previous_batch else None)

        validated_data = serializer.validated_data

        print(validated_data)

        batch = Batch.objects.create(
            batch_number=batch_number,
            purchase_currency_id=validated_data.get("purchase_currency_code"),
            selling_currency_id=validated_data.get("selling_currency_code"),
            created_by=self.request.user
        )

        BatchItem.objects.bulk_create([
            BatchItem(
                batch_id=batch.id,
                vehicle_id=bi.get("vehicle_id"),
                quantity=bi.get("quantity"),
                total_cost_price=bi.get("total_cost_price"),
                unit_price_id=bi.get("unit_price_id"),
                created_by=self.request.user
            ) for bi in validated_data.get("batch_items")
        ])
        return Response({"message": "Batch created successfully"}, status=201)

    
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