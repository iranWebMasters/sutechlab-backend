from rest_framework import serializers
from orders.models import TemporaryRequest, SampleInfo, ExperimentInfo

class TemporaryRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryRequest
        fields = ['id', 'user', 'step', 'description', 'sample_info', 'experiment_info', 'additional_info', 'finalized', 'created_at', 'updated_at']

class SampleInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleInfo
        fields = '__all__'

class ExperimentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentInfo
        fields = '__all__'
















# from rest_framework import serializers
# from services.models import *
# from orders.models import *

# class RequestInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RequestInfo
#         fields = ['id', 'user', 'submission_date', 'description','experiment']
#         read_only_fields = ['id', 'submission_date', 'user',]

#     def create(self, validated_data):
#         user = self.context['request'].user.profile
#         request_info = RequestInfo.objects.create(user=user, **validated_data)
#         return request_info

#     def update(self, instance, validated_data):
#         instance.description = validated_data.get('description', instance.description)
#         instance.save()
#         return instance
    
# class SampleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Sample
#         fields = ['id', 'name', 'description','is_returnable']

# class SampleInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SampleInfo
#         fields = [
#             'sample_type',
#             'sample_amount',
#             'sample_unit',
#             'additional_info',
#             'is_perishable',
#             'expiration_date',
#             'sample_return',
#             'storage_duration',
#             'storage_unit'
#         ]