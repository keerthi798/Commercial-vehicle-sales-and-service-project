from django.contrib import admin
# from .models import CustomUser # Import your model

# admin.site.register(CustomUser)  # Register your model with the admin interface
from django.contrib.auth import get_user_model

User = get_user_model()

class SuperuserAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return User.objects.filter(is_superuser=False)
    list_display=('username','email')

# Register the custom admin class
admin.site.register(User,SuperuserAdmin)