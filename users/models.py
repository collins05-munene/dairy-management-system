from django.db import models
from django.core .validators import RegexValidator

# Create your models here.
name_regex = RegexValidator(
    regex=r'^[a-zA-Z]$',
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
    

class Farmer(models.Model):
    STATUS_CHOICES = [('Active', 'active'), ('Suspended', 'suspended'), ('Pregnancy Leave', 'pregnancy leave')]


    first_name = models.CharField(validators=[name_regex], max_length=30)
    middle_name = models.CharField(validators=[name_regex], max_length=30, blank=True)
    last_name = models.CharField(validators=[name_regex], max_length=30)
    phone_number = models.IntegerField(validators=[number_regex],)
    number_of_cows = models.IntegerField(null=False)
    route_or_location = models.ForeignKey(Route, null=False, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.first_name
    

class Collector(models.Model):
    STATUS_CHOICES = [('Active', 'active'), ('Suspended', 'suspended'), ('Work Leave', 'work leave')]

    first_name = models.CharField(validators=[name_regex], max_length=30)
    middle_name = models.CharField(validators=[name_regex], max_length=30, blank=True)
    last_name = models.CharField(validators=[name_regex], max_length=30)
    phone_number = models.IntegerField(validators=[number_regex],)
    collection_area = models.ForeignKey(Route, null=False, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name
    

class Clerk(models.Model):
    STATUS_CHOICES = [('Active', 'active'), ('Suspended', 'suspended'), ('Work Leave', 'work leave')]

    first_name = models.CharField(validators=[name_regex], max_length=30)
    middle_name = models.CharField(validators=[name_regex], max_length=30, blank=True)
    last_name = models.CharField(validators=[name_regex], max_length=30)
    phone_number = models.IntegerField(validators=[number_regex],)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name
    

class Admin(models.Model):
    STATUS_CHOICES = [('Active', 'active'), ('Suspended', 'suspended'), ('Work Leave', 'work leave')]

    first_name = models.CharField(validators=[name_regex], max_length=30)
    middle_name = models.CharField(validators=[name_regex], max_length=30, blank=True)
    last_name = models.CharField(validators=[name_regex], max_length=30)
    phone_number = models.IntegerField(validators=[number_regex],)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name