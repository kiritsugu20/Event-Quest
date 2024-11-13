from django.db import models

class Hall(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True, null=True)  # Optional
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

class Booking(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField()  # Duration in hours
    purpose = models.TextField()

    def __str__(self):
        return f"{self.hall.name} booked by {self.name} on {self.date} at {self.time}"
