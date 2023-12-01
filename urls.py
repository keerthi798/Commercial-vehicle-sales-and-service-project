from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from.import views
from .models import CartItem
from django.contrib.auth import views as auth_views
 


urlpatterns = [
   path('',views.index,name="index"),
   path('signup/',views.signup, name="signup"),
   path('login/', views.login, name="login"),
   path('dashboard/',views.dashboard,name="dashboard"),
   path('logout/', views.logout_confirm,name='logout'),
    path('change_password/', views.change_password, name='change_password'),
   path('partsorder.html', views.partsorder, name='partsorder'),
   
   path('customer_dash/', views.customer_dash, name='customer_dash'),
   path('parts_list/', views.parts_list, name='parts_list'),

   path('admindashboard/userprofile/', views.admindashboard, name='admindashboard'),
   
   path('servicebranchdashboard/', views.servicebranchdashboard, name='servicebranchdashboard'),
   path('deliveryboydashboard/', views.deliveryboydashboard, name='deliveryboydashboard'),
   path('partsmanagerdashboard/', views.partsmanagerdashboard, name='partsmanagerdashboard'),
   
   path('userdetails/', views.userdetails, name='userdetails'),
   path('service_branch/', views.service_branch, name='service_branch'),
   path('userprofile/', views.userprofile, name='userprofile'),
   
   path('delete_part/<int:part_id>/', views.delete_part, name='delete_part'),
   path('delete_branch/<int:user_id>/', views.delete_branch, name='delete_branch'),
    path('update_part/<int:part_id>/', views.update_part, name='update_part'),
    path('parts_add/', views.parts_add, name='parts_add'),

     path('add_worker/', views.add_worker, name='add_worker'),


    path('parts_managers/', views.parts_managers, name='parts_managers'),

    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),

    path('view_cart/', views.view_cart, name='view_cart'),
    path('view_wishlist/', views.view_wishlist, name='view_wishlist'),
   
    path('all_products/', views.all_products, name='all_products'),

    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('booking/', views.booking, name='booking'),
    path('booking/confirm/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),
    path('booking/reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),


     path('buy_now/<int:product_id>/', views.buy_now_view, name='buy_now'),

    path('edit_profile/', views.edit_profile, name='edit_profile'),
   
    path('download-parts-list/', views.download_parts_list, name='download_parts_list'),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

    path('filter_by_price/', views.filter_by_price, name='filter_by_price'),
    
]