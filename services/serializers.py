from rest_framework import serializers
from .models import *

class UnitAmountSerializer(serializers.ModelSerializer):
    unit_display = serializers.SerializerMethodField()  # فیلد جدید برای نمایش واحد

    class Meta:
        model = Unit_amount  # فرض بر این است که این مدل را از کد شما داریم
        fields = ['id', 'amount', 'unit', 'unit_display']  # اضافه کردن unit_display به fields

    def get_unit_display(self, obj):
        return obj.get_unit_display()  # استفاده از متد get_unit_display

class UnitPriceSerializer(serializers.ModelSerializer):
    currency_display = serializers.SerializerMethodField()  # فیلد جدید برای نمایش واحد پول

    class Meta:
        model = Unit_price
        fields = ['id', 'unit_price', 'currency', 'currency_display']  # اضافه کردن currency_display به fields

    def get_currency_display(self, obj):
        return obj.get_currency_display()  # استفاده از متد get_currency_display

class ParametersSerializer(serializers.ModelSerializer):
    unit_amount = UnitAmountSerializer()
    unit_price = UnitPriceSerializer()
    unit_display = serializers.SerializerMethodField()  # فیلد جدید برای نمایش واحد

    class Meta:
        model = Parameters
        fields = ['id', 'name', 'unit', 'unit_display', 'laboratory', 'unit_amount', 'unit_price']

    def get_unit_display(self, obj):
        return obj.get_unit_display()  # استفاده از متد get_unit_display

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
