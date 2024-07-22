# reservations/models.py

from django.db import models
from django.contrib.auth.models import User

class Route(models.Model):
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    duration = models.DurationField()

    def __str__(self):
        return f"{self.start_point} to {self.end_point}"

class Bus(models.Model):
    operator = models.CharField(max_length=100)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    available_seats = models.IntegerField()
    fare = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.operator} - {self.route}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seats_reserved = models.IntegerField()
    booking_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.bus}"
