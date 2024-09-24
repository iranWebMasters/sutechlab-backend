from rest_framework import serializers
from services.models import *
from orders.models import *

class RequestInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestInfo
        fields = ['id', 'user', 'submission_date', 'description','experiment']
        read_only_fields = ['id', 'submission_date', 'user',]

    def create(self, validated_data):
        user = self.context['request'].user.profile
        request_info = RequestInfo.objects.create(user=user, **validated_data)
        return request_info

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance