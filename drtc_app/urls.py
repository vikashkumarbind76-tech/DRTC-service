from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('api/booking/create/', views.api_create_booking, name='api_create_booking'),
    path('api/calculate-quote/', views.api_calculate_quote, name='api_calculate_quote'),
    path('api/contact/', views.api_contact, name='api_contact'),
    path('api/live-stats/', views.api_live_stats, name='api_live_stats'),
    path('api/booking/status/<str:booking_id>/', views.api_booking_status, name='api_booking_status'),
    path('booking/success/<str:booking_id>/', views.booking_success_view, name='booking_success'),
    path('booking/track/', views.booking_track_view, name='booking_track'),
]
