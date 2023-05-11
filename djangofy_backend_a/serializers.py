from .models import User, UserProjects
from rest_framework import serializers 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = '__all__'
        
class UserProjectsSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = UserProjects 
        fields = '__all__'