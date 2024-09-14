from rest_framework import serializers
from .models import *

class UnitAmountSerializer(serializers.ModelSerializer):
    unit_display = serializers.SerializerMethodField()

    class Meta:
        model = Unit_amount 
        fields = ['id', 'amount', 'unit', 'unit_display'] 

    def get_unit_display(self, obj):
        return obj.get_unit_display()  

class UnitPriceSerializer(serializers.ModelSerializer):
    currency_display = serializers.SerializerMethodField()  
    class Meta:
        model = Unit_price
        fields = ['id', 'unit_price', 'currency', 'currency_display'] 

    def get_currency_display(self, obj):
        return obj.get_currency_display()

class ParametersSerializer(serializers.ModelSerializer):
    unit_amount = UnitAmountSerializer()
    unit_price = UnitPriceSerializer()
    unit_display = serializers.SerializerMethodField() 

    class Meta:
        model = Parameters
        fields = ['id', 'name', 'unit', 'unit_display', 'laboratory', 'unit_amount', 'unit_price']

    def get_unit_display(self, obj):
        return obj.get_unit_display()  

class StandardsSerializer(serializers.ModelSerializer):
    parameters = ParametersSerializer(many=True)  

    class Meta:
        model = Standards
        fields = '__all__'

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = '__all__'

class TestsSerializer(serializers.ModelSerializer):
    standards = StandardsSerializer(many=True) 

    class Meta:
        model = Tests
        fields = '__all__'
