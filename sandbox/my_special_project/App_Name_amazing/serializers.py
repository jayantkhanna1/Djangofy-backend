from rest_framework import serializers 
from .models import Modal_1
from .models import new_modela_1

class Modal_1Serializer(serializers.ModelSerializer): 
    class Meta: 
        model = Modal_1 
        fields = '__all__' 
class new_modela_1Serializer(serializers.ModelSerializer): 
    class Meta: 
        model = new_modela_1 
        fields = '__all__' 
