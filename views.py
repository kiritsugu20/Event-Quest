from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Hall, Booking
from django.utils.timezone import datetime
from datetime import datetime, timedelta
import json

# Registration View
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        email = request.POST.get('email')

        # Basic validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        try:
            # Create a new user
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error occurred: {str(e)}")
            return redirect('register')

    return render(request, 'events/RegistrationForm.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('homepage')  # Redirect to homepage after login
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'events/LoginPage.html')

# Homepage View
def homepage(request):
    return render(request, 'events/homepage.html')

#Hall Booking view
def book_hall(request):
    if request.method == 'POST':
        # Parse JSON data from request body
        try:
            data = json.loads(request.body)
            hall_name = data.get('hall_name')
            name = data.get('name')
            email = data.get('email')
            phone = data.get('phone')
            date = data.get('date')
            time = data.get('time')
            duration = int(data.get('duration'))
            purpose = data.get('purpose')
            
            # Fetch hall instance
            hall = Hall.objects.get(name=hall_name)
            
            # Save booking data
            Booking.objects.create(
                hall_name=hall_name,
                name=name,
                email=email,
                phone=phone,
                date=date,
                time=time,
                duration=duration,
                purpose=purpose
            )

            return redirect('check_availability' , hall_name=hall_name, date=date, time=time)  # Redirect to check availability page after booking
        except (json.JSONDecodeError, KeyError, Hall.DoesNotExist) as e:
            # Handle possible errors such as invalid JSON or missing fields
            return JsonResponse({'error': str(e)}, status=400)
    halls = Hall.objects.all()
    return render(request, 'events/HallBooking.html', {'halls': halls})

def check_availability(request):
    if request.method == 'POST':
        date = request.POST['date']
        time = request.POST['time']

        # Parse input data
        request_time = datetime.strptime(time, '%H:%M').time()

        # Get all halls and their booking status for the given date and time
        available_halls = []
        for hall in Hall.objects.all():
            overlapping_bookings = Booking.objects.filter(
                hall=hall,
                date=date,
            )
            available = True

            for booking in overlapping_bookings:
                booking_start_time = datetime.combine(booking.date, booking.time)
                booking_end_time = booking_start_time + timedelta(hours=booking.duration)
                requested_start_time = datetime.combine(datetime.strptime(date, '%Y-%m-%d'), request_time)
                requested_end_time = requested_start_time + timedelta(hours=1)  # Assuming 1-hour duration for the request

                # Check if there's an overlap in the times
                if (requested_start_time < booking_end_time and requested_end_time > booking_start_time):
                    available = False
                    break

            if available:
                available_halls.append(hall)

        return render(request, 'events/check_availability.html', {'available_halls': available_halls, 'date': date, 'time': time})

    return render(request, 'events/CheckAvailability.html')