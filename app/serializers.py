from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'is_factura', 'contragent', 'nomeclarture', 'qty', 'date', 'nomenclarture_type', 'transport')    