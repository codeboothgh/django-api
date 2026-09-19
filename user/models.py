from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db.models.functions import UUID4, Now
from django.conf import settings

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("email is required")

        if not first_name or not last_name:
            raise ValueError("First name and last name is required")

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True

        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        db_default=UUID4(),
        primary_key=True,
        unique=True
    )
    first_name = models.CharField(
        max_length=255,
        blank=True, null=True
    )
    last_name = models.CharField(
        max_length=255,
        blank=True, null=True
    )
    email = models.EmailField(
        max_length=255, unique=True
    )
    date_joined = models.DateTimeField(
        db_default=Now(),
    )
    phone = models.CharField(
        max_length=100,
        blank=True, null=True
    )
    is_staff = models.BooleanField(
        default=False,
    )
    is_active = models.BooleanField(
        default=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        db_table = 'user'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

#this are fields that most of the model will have so write them here not repeat those on each model
# so my model will inherit from this  class 
# with this ( abstract = True) the AbstractFields will not get it own databse
class AbstractFields(models.Model):
    id = models.UUIDField(
        db_default=UUID4(), # this tells the databse to generate a new uuid when a new record is created
        primary_key=True,
        unique=True
    )

    # a slug is normally a URL-friendly version of something.i want to do something like Toyota corolla will toyota-corolla
    slug = models.SlugField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(
        db_default=Now()
    )
    created_by = models.ForeignKey( # this stores the user who created this records
        settings.AUTH_USER_MODEL,
        to_field="id",
        on_delete=models.SET_NULL, #If the user who created the record is delete, dont delete the brand.just remove the connection to that user
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_ownership"
    )

    class Meta:
        abstract = True