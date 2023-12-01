from django import forms
from .models import CustomUser


from .models import Parts
# from .models import ServiceBooking

# class ServiceBookingForm(forms.ModelForm):
#     class Meta:
#         model = ServiceBooking
#         fields = ['user', 'driver_number', 'vehicle_number', 'service_branch', 'vehicle_model', 'service_type', 'service_date', 'email']

class PartForm(forms.ModelForm):
    class Meta:
        model = Parts
        fields = ['partsname', 'description', 'price', 'parts_image', 'quantity','category', 'subcategory']
class WorkerForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email','address','phone_number','password','role']

