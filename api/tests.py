from django.test import TestCase
from .models import Risk, Field, FieldType, FieldTypeValues, FieldTypeEnumValues
from .serializers import RiskSerializer, FieldSerializer
import json

class RiskModelTestCase(TestCase):
    
    def setUp(self):
        self.num_field_name = "prize"
        self.num_field_value = "12345"
        self.num_field_type = FieldType(type = FieldTypeValues.NUMBER)
        self.num_field_type.save()
        self.field_num = Field(name = self.num_field_name, value = self.num_field_value, field_type = self.num_field_type)
       
        self.txt_field_name = "hacking"
        self.txt_field_value = "DoS attack"
        self.txt_field_type = FieldType(type = FieldTypeValues.TEXT)
        self.txt_field_type.save()
        self.field_txt = Field(name = self.txt_field_name, value = self.txt_field_value, field_type = self.txt_field_type)

        self.risk_1 = Risk(name = "Test Risk 1")
        self.fields = []   

    def test_risk_can_be_added(self):
        old_count = Risk.objects.count()
        self.risk_1.save()
        new_count = Risk.objects.count()
        self.assertNotEqual(old_count, new_count)
    
    def test_Fields_can_be_added_to_risk(self):
              
        self.field_num.save()
        self.fields.append(self.field_num) 
        
        self.field_txt.save()
        self.fields.append(self.field_txt) 

        self.risk_1.save()       
        self.risk_1.fields.set(self.fields)

        self.assertEqual(self.risk_1.fields.all()[0].name, self.num_field_name)
        self.assertEqual(self.risk_1.fields.all()[0].value, self.num_field_value)
        self.assertEqual(self.risk_1.fields.all()[0].field_type.type, FieldTypeValues.NUMBER)

        self.assertEqual(self.risk_1.fields.all()[1].name, self.txt_field_name)
        self.assertEqual(self.risk_1.fields.all()[1].value, self.txt_field_value)
        self.assertEqual(self.risk_1.fields.all()[1].field_type.type, FieldTypeValues.TEXT)
    

class GetRiskTypesTestCase(TestCase):


    def setUp(self):
        self.risk_name_1 = "Test Risk 1"
        self.risk_name_2 = "Test Risk 2"
        self.risk_1 = Risk(name = self.risk_name_1)
        self.risk_2 = Risk(name = self.risk_name_2)

        self.num_field_name = "prize"
        self.num_field_value = "12345"
        self.num_field_type = FieldType(type = FieldTypeValues.NUMBER)
        self.num_field_type.save()
        self.field_num = Field(name = self.num_field_name, value = self.num_field_value, field_type = self.num_field_type)
       
        self.txt_field_name = "hacking"
        self.txt_field_value = "DoS attack"
        self.txt_field_type = FieldType(type = FieldTypeValues.TEXT)
        self.txt_field_type.save()
        self.field_txt = Field(name = self.txt_field_name, value = self.txt_field_value, field_type = self.txt_field_type)

        self.enum_field_name = 'lov'
        self.enum_field_type = FieldType(type = FieldTypeValues.ENUM)
        self.enum_field_type.save()
        self.field_enum = Field(name = self.enum_field_name, field_type = self.enum_field_type)
        
        self.enum_field_type_value_1 = "choice1"
        self.enum_field_type_value_2 = "choice2"
        self.enum_field_type_value_3 = "choice3"
        self.enum_field_choice_1 = FieldTypeEnumValues(enum_value = self.enum_field_type_value_1)
        self.enum_field_choice_2 = FieldTypeEnumValues(enum_value = self.enum_field_type_value_2)
        self.enum_field_choice_3 = FieldTypeEnumValues(enum_value = self.enum_field_type_value_3)
        
        self.fields = []   

    def test_get_all_risk_types(self):
        
        self.field_num.save()
        self.fields.append(self.field_num) 
        
        self.field_txt.save()
        self.fields.append(self.field_txt) 

        self.field_enum.save();
        self.fields.append(self.field_enum) 
                
        self.enum_field_choice_1.field_associated_with_enum = self.field_enum
        self.enum_field_choice_2.field_associated_with_enum = self.field_enum
        self.enum_field_choice_3.field_associated_with_enum = self.field_enum
        self.enum_field_choice_1.save()
        self.enum_field_choice_2.save()
        self.enum_field_choice_3.save()

        self.risk_1.save()       
        self.risk_1.fields.set(self.fields)
    
        self.risk_2.save()       
        self.risk_2.fields.set(self.fields)

        response = self.client.get("/api/getAllRiskTypes/")
        self.assertEqual(response.status_code, 200)

        riskResponse = json.loads(response.content)
        
        self.assertEqual(riskResponse[0]["name"],self.risk_name_1)
        self.assertEqual(riskResponse[0]["fields"][0]["name"],self.num_field_name)
        self.assertEqual(riskResponse[0]["fields"][0]["field_type"],FieldTypeValues.NUMBER.label)

        self.assertEqual(riskResponse[0]["fields"][1]["name"],self.txt_field_name)
        self.assertEqual(riskResponse[0]["fields"][1]["field_type"],FieldTypeValues.TEXT.label)

        self.assertEqual(riskResponse[0]["fields"][2]["name"],self.enum_field_name)
        self.assertEqual(riskResponse[0]["fields"][2]["field_type"],FieldTypeValues.ENUM.label)
        self.assertEqual(riskResponse[0]["fields"][2]["enum_values"][0]["enum_value"],self.enum_field_choice_1.enum_value)
        self.assertEqual(riskResponse[0]["fields"][2]["enum_values"][1]["enum_value"],self.enum_field_choice_2.enum_value)
        self.assertEqual(riskResponse[0]["fields"][2]["enum_values"][2]["enum_value"],self.enum_field_choice_3.enum_value)

        self.assertEqual(riskResponse[1]["name"],self.risk_name_2)
        self.assertEqual(riskResponse[1]["fields"][0]["name"],self.num_field_name)
        self.assertEqual(riskResponse[1]["fields"][1]["name"],self.txt_field_name)
    
    def test_get_specific_risk_type(self):
        self.risk_1.save()                
        self.risk_2.save()       
        
        response = self.client.get("/api/getRiskType/" + self.risk_name_2)
        self.assertEqual(response.status_code, 200)

        riskResponse = json.loads(response.content)
        self.assertEqual(riskResponse[0]["name"],self.risk_name_2)