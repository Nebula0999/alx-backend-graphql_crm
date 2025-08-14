from django.db import models

# Create your models here.
class User(models.Model):
    """
    Model representing a user in the CRM system.
    """
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.username

class Booking(models.Model):
    """
    Model representing a booking in the CRM system.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateTimeField()
    description = models.TextField(blank=True)
