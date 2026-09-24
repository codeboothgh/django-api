from django.db import models

from customer.models import Customer
from user.models import AbstractFields
from vehicle.models import Currency, Vehicle, VehiclePrice

# Create your models here.

class Batch(AbstractFields):
    batch_number = models.CharField(max_length=255, unique=True)
    purchase_currency = models.ForeignKey(Currency, related_name="batch_purchase_currency", on_delete=models.SET_NULL, blank=True, null=True)
    selling_currency = models.ForeignKey(Currency, related_name="batch_selling_currency", on_delete=models.SET_NULL, blank=True, null=True)

class BatchItem(AbstractFields):
    vehicle = models.ForeignKey(Vehicle, related_name="batch_item_vehicle", on_delete=models.SET_NULL, blank=True, null=True)
    batch = models.ForeignKey(Batch, related_name="batch_item_batch", on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField(db_default=0, blank=True, null=True)
    total_cost_price = models.DecimalField(db_default=0.0, decimal_places=2, max_digits=10, blank=True, null=True)

    @property
    def unit_price(self):
        try:
            unit_price = self.total_cost_price / self.quantity
            return unit_price
        except:
            return 0


class Order(AbstractFields):
    PAYMENT_STATUS = [
        (0, "Not Paid"),
        (1, "Part Paid"),
        (2, "Fully Paid")
    ]
    STATUS = [
        ('PENDING', 'Pending'),
        ('SOLD', 'Sold'),
        ('RETURNED', 'Returned'),
        ('CANCELLED', 'Cancelled')
    ]

    order_number = models.CharField(max_length=255, unique=True)
    customer = models.ForeignKey(Customer, related_name="sale_customer", on_delete=models.SET_NULL, blank=True, null=True)
    payment_status = models.IntegerField(choices=PAYMENT_STATUS, db_default=0)
    status = models.CharField(choices=STATUS, max_length=255, db_default="PENDING")

class OrderItem(AbstractFields):
    order = models.ForeignKey(Order, related_name="order_item_order", on_delete=models.CASCADE, blank=True, null=True)
    vehicle = models.ForeignKey(Vehicle, related_name="order_item_vehicle", on_delete=models.SET_NULL, blank=True, null=True)
    selling_price = models.ForeignKey(VehiclePrice, related_name="order_item_selling_price", on_delete=models.SET_NULL, blank=True, null=True)
    actual_selling_price = models.DecimalField(db_default=0.0, decimal_places=2, max_digits=10, blank=True, null=True)
    quantity = models.PositiveIntegerField(db_default=1)


class Payment(AbstractFields):
    order = models.ForeignKey(Order, related_name="payment_order", on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(db_default=0.0, decimal_places=2, max_digits=10, blank=True, null=True)
    payment_method = models.CharField(max_length=255, blank=True, null=True)
    currency = models.ForeignKey(Currency, related_name="payment_currency", on_delete=models.SET_NULL, blank=True, null=True)

