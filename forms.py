from django import forms
from .models import Parts
from .models import ServiceBooking

class ServiceBookingForm(forms.ModelForm):
    class Meta:
        model = ServiceBooking
        fields = '__all__'
class PartForm(forms.ModelForm):
    class Meta:
        model = Parts
        fields = ['partsname', 'description', 'price', 'parts_image', 'quantity']

