from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from allauth.socialaccount.models import SocialAccount,SocialApp
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import ServiceBooking
from .forms import ServiceBookingForm
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
from .models import ServiceBooking
from .forms import PartForm
from .models import Parts,CartItem, WishlistItem
from .models import CustomUser
import re
from django.http import Http404


  # Ensure the correct import path for CustomUser model

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        address = request.POST['address']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST['role'] 
        if not username:
            error_message = 'Username is required.'
            return render(request, 'signup.html', {'error_message': error_message})

        if not username[0].isupper():
            error_message = 'Username must start with a capital letter.'
            return render(request, 'signup.html', {'error_message': error_message})

        if not re.match(r'^[A-Z][a-zA-Z0-9]{0,9}$', username):
            error_message = 'Username can only contain uppercase letters followed by lowercase letters, characters, and numbers (maximum 10 characters).'
            return render(request, 'signup.html', {'error_message': error_message})

        if ' ' in username:
            error_message = 'Username cannot contain white spaces.'
            return render(request, 'signup.html', {'error_message':error_message})


        # Check if the email already exists in the database
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error_message': 'Email address is already in use.'})
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error_message': 'username is already in use.'})
        if password != confirm_password:
            return render(request, 'signup.html', {'error_message': 'Passwords do not match'})

        # Create a new user object
        user = CustomUser.objects.create_user(username=username,email=email, address=address, phone_number=phone_number,password=password, role=role)
        
        # Store user ID in the session
       
        # Redirect to the dashboard after successful registration
        return redirect('login')

    return render(request, 'signup.html')
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)  # Log in the user
            request.session['username'] = username

            if user.role == "service_center":
                return redirect("servicebranchdashboard")
            elif user.role == "user":
                return redirect("index")
            elif user.username == "keerthisree":
                return redirect("admindashboard")
            elif user.role == "parts_manager":
                return redirect("partsmanagerdashboard")          
        else:
            messages.error(request, "Incorrect username or password. Please try again.")

    return render(request, 'login.html')

def logout_confirm(request):
    if request.user.is_authenticated:
          # Remove your custom session data
        
        # Clear any Google-related session data if you have stored it
       
        logout(request)
    return render(request, 'logout_confirm.html')


def dashboard(request):
    return render(request, 'index.html') 
    # Use session data to retrieve the user object
def booking(request):
    if request.method == 'POST':
        form = ServiceBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # Assuming you are using user authentication
            booking.save()
            success_message = "Service booking has been successfully updated."
            return redirect('index')  # Redirect to a success page or your desired URL
    else:
        form = ServiceBookingForm()
    bookings = ServiceBooking.objects.filter(user=request.user)
    return render(request, 'booking.html', {'form': form, 'bookings': bookings})


def partsorder(request):
      # Redirect to the booking page after form submission
    parts_orders = Parts.objects.all()  # Query all the added parts
    return render(request, 'partsorder.html', {'parts_orders': parts_orders})

   
def customer_dash(request):
    # Retrieve data or perform any necessary actions here
    # Example: data = YourModel.objects.all()

    return render(request, 'customer_dash.html')

def admindashboard(request):
    users = CustomUser.objects.all()
    
    return render(request, 'admindashboard.html', {'users': users})
   
       


def servicebranchdashboard(request):
    
    # Your view logic goes here
    return render(request, 'servicebranchdashboard.html')
def deliveryboydashboard(request):
    # Your view logic goes here
    return render(request, 'deliveryboydashboard.html')
def partsmanagerdashboard(request):
    # Your view logic goes here
    return render(request, 'partsmanagerdashboard.html')

def userdetails(request):
     bookings = ServiceBooking.objects.all()

     return render(request, 'userdetails.html', {'bookings': bookings})
  
    # Your view logic goes here

def service_branch(request):
    # Fetch users with the "Worker" role
    service_center = CustomUser.objects.filter(role='service_center')

    return render(request, 'service_branch.html', {'service_center': service_center})

def userprofile(request):
    # Fetch users with the "Worker" role
    users = CustomUser.objects.filter(role='user')
    return render(request, 'userprofile.html', {'users': users})

def parts_managers(request):
    # Fetch users with the "Worker" role
    parts_managers = CustomUser.objects.filter(role='parts_manager')

    return render(request, 'parts_managers.html', {'parts_managers': parts_managers})

    
def parts_add(request):
    if request.method == 'POST':
        form = PartForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('parts_add')
    else:
        form = PartForm()
    
    return render(request, 'parts_add.html', {'form': form})
def parts_list(request):
    parts_orders = Parts.objects.all()  # Query all the added parts
    return render(request, 'parts_list.html', {'parts_orders': parts_orders})
def delete_part(request, part_id):
    if request.method == 'POST':
        parts = Parts.objects.get(pk=part_id)
        parts.delete()
    return redirect('parts_list')
    
def update_part(request, part_id):
    parts = get_object_or_404(Parts, id=part_id)

    if request.method == 'POST':
        form = PartForm(request.POST, request.FILES, instance=parts)
        if form.is_valid():
            form.save()
            return redirect('parts_list')  # Redirect to the parts list page after updating
    else:
        form = PartForm(instance=parts)

    return render(request, 'update_part.html', {'form': form, 'parts': parts})

def delete_branch(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, pk=user_id)
        user.delete()
    return redirect('service_branch')
def download_parts_list(request):
    # Query all the added parts
    parts_orders = Parts.objects.all()

    # Create a response with PDF content
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="parts_list.pdf"'

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Create a list to hold table data
    table_data = [['Part ID', 'Part Name', 'Description', 'Image']]

    for part in parts_orders:
        row = [part.id, part.partsname, part.description, '']
        if part.parts_image:  # Adjust the field name for the image
            image_path = part.parts_image.path
            image = Image(image_path, width=50, height=50)
            row[-1] = image

        table_data.append(row)

    # Create the table and set styles
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Build the PDF document
    doc.build([table])

    return response
@login_required
def add_to_cart(request, product_id):
    # Retrieve the product and user
    product = Parts.objects.get(id=product_id)
    user = request.user

    # Check if the product is already in the user's cart
    cart_item, created = CartItem.objects.get_or_create(user=user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return JsonResponse({'success': True})

@login_required
def view_cart(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    return render(request, 'view_cart.html', {'cart_items': cart_items})

@login_required
def view_wishlist(request):
    user = request.user
    wishlist_items = WishlistItem.objects.filter(user=user)
    return render(request, 'view_wishlist.html', {'wishlist_items': wishlist_items})
def add_to_wishlist(request, product_id):
    try:
        product = Parts.objects.get(pk=product_id)
    except Parts.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'})

    # Check if the product is already in the user's wishlist
    if WishlistItem.objects.filter(user=request.user, product=product).exists():
        return JsonResponse({'success': False, 'message': 'Product is already in your wishlist'})

    # If the product is not in the wishlist, add it
    WishlistItem.objects.create(user=request.user, product=product)

    return JsonResponse({'success': True, 'message': 'Product added to your wishlist'})
  # Redirect to your cart view
def all_products(request):
    products = products.objects.all()  # Retrieve all products
    return render(request, 'all_products.html', {'products': products})

def remove_from_cart(request, product_id):
    # Assuming your CartItem model has a unique identifier field, e.g., id
    try:
        cart_items = CartItem.objects.get(id=product_id)
        cart_items.delete()
        success = True
    except CartItem.DoesNotExist:
        success = False

    return JsonResponse({'success': success})
def confirm_booking(request, booking_id):
    try:
        booking = ServiceBooking.objects.get(pk=booking_id)
    except ServiceBooking.DoesNotExist:
        raise Http404("Booking does not exist")
    booking.status = 'Confirmed'
    booking.save()
    subject = 'Booking Confirmation'
    message = 'Your booking has been confirmed.'
    from_email = 'keerthisree798@gmail.com'  # Replace with your email address
    recipient_list = [booking.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return redirect('userdetails')

def reject_booking(request, booking_id):
    try:
        booking = ServiceBooking.objects.get(pk=booking_id)
    except ServiceBooking.DoesNotExist:
        raise Http404("Booking does not exist")
    booking.status = 'Rejected'
    booking.save()
    subject = 'Booking Rejection'
    message = 'Your booking has been rejected.'
    from_email = 'keerthisree798@gmail.com'  # Replace with your email address
    recipient_list = [booking.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return redirect('userdetails')