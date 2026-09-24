from django.db import models

from user.models import AbstractFields

# Create your models here.

class Customer(AbstractFields):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=100, blank=True, null=True)
    national_id = models.CharField(max_length=255, blank=True, null=True)


