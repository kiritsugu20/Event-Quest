from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('book-hall/', views.hall_booking, name='book_hall'),
    path('check-availability/', views.check_availability, name='check_availability'),
]
