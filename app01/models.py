from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    phone_number = models.CharField(
        max_length=15, unique=True, blank=True, null=True
    )
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    signature = models.TextField(null=True, blank=True)


class Course(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses",
    )
    name = models.CharField(max_length=100)
    day_of_week = models.CharField(max_length=10)  # 1=Monday, 7=Sunday
    time_slot = models.CharField(
        max_length=2
    )  # Slot number for the time (e.g., 1st, 2nd period)
    color = models.CharField(max_length=20, default="blue")

    class Meta:
        unique_together = ("user", "day_of_week", "time_slot")

    def __str__(self):
        return f"{self.name} on day {self.day_of_week} at time slot {self.time_slot}"
