from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
import binascii
import os

# Create your models here.
name_regex = RegexValidator(
    regex=r'^[a-zA-Z]+$',
    message="Farmer's name can only be in letters"
)
number_regex = RegexValidator(
    regex=r'^(?:\+2547|\+2541|07|01)\d{8}$',
    message='Incorrect phone number format'
)
class Route(models.Model):
    route_name = models.CharField(validators=[name_regex], max_length=45)

    def __str__(self):
        return self.route_name

class UserMixin(models.Model):
    STATUS_CHOICES = [('Active', 'active'), ('Suspend', 'suspended')]

    first_name = models.CharField(validators=[name_regex], max_length=50)
    middle_name = models.CharField(validators=[name_regex], max_length=50, blank=True)
    last_name = models.CharField(validators=[name_regex], max_length=50)
    phone_number = models.CharField(validators=[number_regex], max_length=15, unique=True)
    password = models.CharField(max_length=128)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Farmer(UserMixin):
    STATUS_CHOICES = [("Active", "active"), ("Suspended", "suspended"), ("Pregnancy Leave", "pregnancy leave")]
    number_of_cows = models.IntegerField()
    route_or_location = models.ForeignKey(Route, on_delete=models.CASCADE)


class Collector(UserMixin):
    STATUS_CHOICES = [('Active', 'active'), ('Suspended', 'suspended'), ('Work Leave', 'work leave')]
    collection_area = models.ForeignKey(Route, on_delete=models.CASCADE)


class Clerk(UserMixin):
    STATUS_CHOICES = [("Active", "active"), ("Suspended", "suspended"), ("Work Leave", "work leave")]


class Admin(models.Model):
    STATUS_CHOICES = [('Active', 'active'), ('Suspended', 'suspended'), ('Work Leave', 'work leave')]


class UserToken(models.Model):
    USER_TYPES = [('admin', 'Admin'), ('clerk', 'Clerk'), ('collector', 'Collector'), ('farmer', 'Farmer')]

    token = models.CharField(max_length=64, unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_token():
        return binascii.hexlify(os.urandom(32)).decode()
    
    def __str__(self):
        return f"{self.user_type}: {self.user_id} - {self.token}"