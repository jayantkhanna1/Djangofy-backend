from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100,null=True,blank=True)
    type_of_user = models.CharField(max_length=100,null=True,blank=True)
    otp = models.CharField(max_length=100,null=True,blank=True)
    otp_verified = models.BooleanField(default=False)
    private_key = models.CharField(max_length=100,null=True,blank=True)
    github_token = models.CharField(max_length=100,null=True,blank=True)