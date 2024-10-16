from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Activity(models.Model):
    ACTIVITY_CHOICES = [
        ('Running', 'Running'),
        ('Cycling', 'Cycling'),
        ('Weightlifting', 'Weightlifting'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    duration = models.PositiveIntegerField()  # in minutes
    distance = models.FloatField()  # in km
    calories_burned = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.date}"

# Signal to create a Token for a new User
@receiver(post_save, sender=User)
def TokenCreate(sender, instance, created, **kwargs):
    # Check if a new user instance was created
    if created:
        Token.objects.create(user=instance)  # Create a token for the newly registered user