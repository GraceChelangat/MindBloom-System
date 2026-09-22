from django.db import models
from django.contrib.auth.models import User


class TeenagerYoungAdult(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teenager_profile'
    )

    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=30, blank=True)
    contact_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name