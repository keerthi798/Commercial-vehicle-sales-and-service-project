from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models

class CustomUser(AbstractUser):
     # Add any additional fields you need
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True) 
    role = models.CharField(max_length=100,default="")
    def change_password(self, new_password):
        self.set_password(new_password)
        self.save()

    def _str_(self):
        return self.username


class ServiceBooking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    driver_number = models.CharField(max_length=15)
    vehicle_number = models.CharField(max_length=15)
    service_branch = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    service_type = models.CharField(max_length=10)
    service_date = models.DateField()
    email = models.EmailField(default='')

    def __str__(self):
        return f"Service Booking for {self.user.email if self.user else 'No User'}"


class Parts(models.Model):
    partsname = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    parts_image = models.ImageField(upload_to='part_images/')
    quantity = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=50, default='Uncategorized') # Add category field
    subcategory = models.CharField(max_length=50,default='Uncategorized')

    def __str__(self):
        return self.partsname
    
class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Parts, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class WishlistItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Parts, on_delete=models.CASCADE)
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    
    def str(self):
         return self.username   
    

    