from django.db import models
from datetime import datetime
# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=100,null=True,blank=True)
    type_of_user = models.CharField(max_length=100,null=True,blank=True)
    otp = models.CharField(max_length=100,null=True,blank=True)
    otp_verified = models.BooleanField(default=False)
    private_key = models.CharField(max_length=100,null=True,blank=True)
    github_token = models.CharField(max_length=100,null=True,blank=True)
    admin = models.BooleanField(default=False)

class UserProjects(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    project_link = models.CharField(max_length=1000,null=True,blank=True)
    project_name = models.CharField(max_length=1000)
    project_data = models.JSONField(null=True,blank=True)
    github_link = models.CharField(max_length=1000,null=True,blank=True)
    github_repo_name = models.CharField(max_length=1000,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



