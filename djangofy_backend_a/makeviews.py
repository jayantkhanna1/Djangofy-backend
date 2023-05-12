class CreateViews:
    def __init__(self,project_name,apps,rest_framework,pagination,email_backend,mobile_backend,static_backend,celery):
        self.project_name = project_name
        self.apps = []
        i=1
        for app in apps:
            self.apps.append(app["app_name_"+str(i)])
            i+=1

        self.rest_framework = rest_framework
        self.pagination = pagination
        self.email_backend = email_backend
        self.mobile_backend = mobile_backend
        self.static_backend = static_backend
        self.celery = celery

    def makeViews(self):
        # Editing views.py file in all apps
        for app in self.apps:
            app = app.replace("'","")
            file = open("sandbox/"+self.project_name + "/" + app + "/views.py","w")
            file.write("from django.shortcuts import render\n")
            file.write("from django.http import HttpResponse\n")
            file.write("from .models import *\n")
            file.write("from django.views.decorators.csrf import csrf_exempt\n")
            file.write("from django.http import JsonResponse\n")
            file.write("import os\n")
            file.write("from dotenv import load_dotenv \n")
            file.write("load_dotenv()\n")
            file.write("import json\n")

            if self.rest_framework:
                file.write("from rest_framework import viewsets\n")
                file.write("from .serializers import *\n")
                file.write("from rest_framework.response import Response\n")
                file.write("from rest_framework import status\n")
                file.write("from rest_framework.decorators import api_view\n")
                file.write("from django.http import Http404\n")
                file.write("from rest_framework import filters, generics\n")
                file.write("from django_filters.rest_framework import DjangoFilterBackend\n")
                file.write("from rest_framework.filters import SearchFilter, OrderingFilter\n")
            
            if self.pagination:
                file.write("from rest_framework import pagination\n")

            if self.email_backend:
                file.write("from django.core.mail import send_mail\n")
                if self.email_backend.lower() == "sendgrid":
                    file.write("from sendgrid import SendGridAPIClient\n")
                    file.write("from sendgrid.helpers.mail import Mail\n")
            
            if self.mobile_backend:
                file.write("from twilio.rest import Client\n")
            
            if self.celery:
                file.write("from .tasks import *\n")
            
            # Need to import boto3 for aws
            if self.static_backend:
                if self.static_backend.lower() == "aws":
                    file.write("import boto3\n")
                    file.write("from botocore.exceptions import NoCredentialsError\n")
                elif self.static_backend.lower() == "gcp":
                    file.write("from google.cloud import storage\n")
                elif self.static_backend.lower() == "azure":
                    file.write("from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient\n")
                else:
                    pass

            file.write("\n")
            file.close()

        return True