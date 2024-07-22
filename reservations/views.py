# reservations/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Bus, Booking, Route
from .forms import UserRegisterForm, BusSearchForm, PasswordChangeCustomForm
from django.core.mail import send_mail
from django.conf import settings
import uuid

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # Activate account immediately
            user.save()
            messages.success(request, 'Your account has been created successfully. You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def activate_account(request, token):
    try:
        user = User.objects.get(profile__activation_token=token)
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully.')
        return redirect('login')
    except User.DoesNotExist:
        messages.error(request, 'Activation link is invalid!')
        return redirect('home')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                login(request, user)
                messages.success(request, f'Welcome, {user.username}')
                return redirect('home')
            else:
                messages.error(request, 'Account not activated. Check your email for the activation link.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def find_bus(request):
    form = BusSearchForm()
    return render(request, 'find_bus.html', {'form': form})

@login_required
def search_results(request):
    if request.method == 'POST':
        form = BusSearchForm(request.POST)
        if form.is_valid():
            from_location = form.cleaned_data['from_location']
            to_location = form.cleaned_data['to_location']
            date = form.cleaned_data['date']
            
            buses = Bus.objects.filter(
                route__start_point=from_location,
                route__end_point=to_location,
                departure_time__date=date
            )

            return render(request, 'search_results.html', {'buses': buses, 'date': date})
    return redirect('find_bus')

@login_required
def select_seats(request, bus_id, date):
    bus = get_object_or_404(Bus, id=bus_id)
    return render(request, 'select_seats.html', {'bus': bus, 'date': date})

@login_required
def booking_confirmation(request, bus_id):
    if request.method == 'POST':
        bus = get_object_or_404(Bus, id=bus_id)
        seats = int(request.POST.get('seats'))

        if seats <= bus.available_seats:
            bus.available_seats -= seats
            bus.save()

            booking = Booking.objects.create(
                user=request.user,
                bus=bus,
                seats_reserved=seats
            )

            messages.success(request, 'Booking successful! Proceed to payment.')
            return redirect('payment', booking_id=booking.id)
        else:
            messages.error(request, 'Not enough available seats.')
            return redirect('select_seats', bus_id=bus.id, date=date)
    return redirect('find_bus')

@login_required
def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'payment.html', {'booking': booking})

@login_required
def confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking_confirmation.html', {'booking': booking})

@login_required
def settings_view(request):
    if request.method == 'POST':
        form = PasswordChangeCustomForm(request.POST)
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            messages.success(request, 'Password changed successfully.')
            return redirect('settings')
    else:
        form = PasswordChangeCustomForm()
    return render(request, 'settings.html', {'form': form})

def about(request):
    return render(request, 'about.html')

def faq(request):
    return render(request, 'faq.html')

def help_view(request):
    return render(request, 'help.html')

