from django.db import models
from enumfields import EnumField
from enumfields import Enum 

class FieldTypeValues(Enum):
    TEXT = 1
    NUMBER = 2
    DATE = 3
    ENUM = 4

    class Labels:
        TEXT = 'text'
        NUMBER = 'number'
        DATE = 'date'
        ENUM = 'enum'

class FieldType(models.Model):
    type = EnumField(FieldTypeValues)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.type
    
    def __unicode__(self):
        return self.type

class Field(models.Model):
    name = models.CharField(max_length=100, blank=False)
    value = models.CharField(max_length=100)
    field_type = models.ForeignKey(FieldType, on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "%s %s" % (self.name, self.value)
    
    def __unicode__(self):
        return "%s %s" % (self.name, self.value)

class FieldTypeEnumValues(models.Model):
    enum_value = models.CharField(max_length=100, blank=False, unique=True)
    field_associated_with_enum = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='enum_values')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.enum_value

class Risk(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    fields = models.ManyToManyField(Field, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return self.name

