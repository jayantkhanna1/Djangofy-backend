from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    type_of_user = models.CharField(max_length=100)
    otp = models.CharField(max_length=100)
    otp_verified = models.BooleanField(default=False)
    private_key = models.CharField(max_length=100)