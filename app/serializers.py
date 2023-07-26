from rest_framework import serializers
from .models import AdvUser, Document
        
class AdvUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvUser
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'