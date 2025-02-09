from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking_detail'),
]