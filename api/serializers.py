from rest_framework import serializers
from .models import Risk, Field, FieldTypeEnumValues, FieldType

class FieldTypeEnumValuesSerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldTypeEnumValues
        fields = ('enum_value', 'date_created', 'date_modified')
        readonly = ('date_created', 'date_modified')

class FieldTypeSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = FieldType
            fields = ('type')


class FieldSerializer(serializers.ModelSerializer):    
    enum_values = FieldTypeEnumValuesSerializer(many=True, read_only=True)
    field_type = serializers.CharField(source='field_type.type')

    class Meta:
        model = Field
        fields = ('name', 'value', 'field_type', 'enum_values', 'date_created', 'date_modified')
        readonly = ('date_created', 'date_modified')
    

class RiskSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True, read_only=True)

    class Meta:
        model = Risk
        fields = ('name', 'fields', 'date_created', 'date_modified')
        readonly = ('date_created', 'date_modified')

