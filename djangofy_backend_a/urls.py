from . import views
from django.urls import path

urlpatterns = [
    path('getZip',views.getZip,name='getZip'),
]
