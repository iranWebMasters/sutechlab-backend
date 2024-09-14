from rest_framework import serializers
from .models import Standards, Sample, Tests, Parameters

class ParametersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameters
        fields = '__all__'

class StandardsSerializer(serializers.ModelSerializer):
    parameters = ParametersSerializer(many=True)  # استفاده از سریالایزر پارامترها

    class Meta:
        model = Standards
        fields = '__all__'

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = '__all__'

class TestsSerializer(serializers.ModelSerializer):
    standards = StandardsSerializer(many=True)  # استفاده از سریالایزر استانداردها

    class Meta:
        model = Tests
        fields = '__all__'
