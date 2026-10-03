from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Batch)
admin.site.register(BatchItem)
admin.site.register([Order, OrderItem, Payment])