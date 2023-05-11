from rest_framework import serializers 
from .models import vb

class vbSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = vb 
        fields = '__all__' 
