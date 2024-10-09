from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from app_smart.models import Sensor, TemperaturaData

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) 

    def create(self, validated_data):    
        validated_data['password'] = make_password(validated_data['password'])
        # Criar e retornar o usuário
        return User.objects.create(**validated_data)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password'] 
        extra_kwargs = {'password': {'write_only': True}}
        

class SensorSerializer(serializers.ModelSerializer):	
    class Meta:		
        model = Sensor		
        fields = '__all__'  # Isso serializa todos os campos do modelo Sensor


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class TemperaturaDataSerializer(serializers.ModelSerializer):
    class Meta:	
        model = TemperaturaData
        fields = '__all__'

        