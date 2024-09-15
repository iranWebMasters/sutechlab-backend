from rest_framework import serializers
from .models import *

class UnitAmountSerializer(serializers.ModelSerializer):
    unit_display = serializers.SerializerMethodField()

    class Meta:
        model = UnitAmount 
        fields = ['id', 'amount', 'unit', 'unit_display'] 

    def get_unit_display(self, obj):
        return obj.get_unit_display()  

class UnitPriceSerializer(serializers.ModelSerializer):
    currency_display = serializers.SerializerMethodField()

    class Meta:
        model = UnitPrice
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
        model = Test
        fields = '__all__'

class LaboratorySerializer(serializers.ModelSerializer):
    faculty = serializers.StringRelatedField()  # Include faculty name
    technical_manager = serializers.StringRelatedField()  # Include technical manager

    class Meta:
        model = Laboratory
        fields = ['id', 'name', 'faculty', 'technical_manager']

class ExperimentSerializer(serializers.ModelSerializer):
    tests = TestsSerializer(many=True)
    laboratory = LaboratorySerializer()

    class Meta:
        model = Experiment
        fields = ['id', 'request_type', 'tests', 'laboratory']
