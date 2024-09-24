from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from services.models import *
from orders.models import *
from .serializers import *
import jdatetime
from rest_framework.parsers import JSONParser
from rest_framework import status



class Page1API(APIView):
    permission_classes = [IsAuthenticated]
    # parser_classes = [JSONParser]

    def get(self, request, pk=None):
        try:
            experiment = Experiment.objects.get(id=pk)
            laboratory = experiment.laboratory
        except Experiment.DoesNotExist:
            return Response({'message': 'This experiment is not available'})

        first_name = request.user.profile.first_name if request.user.is_authenticated else 'مهمان'
        last_name = request.user.profile.last_name if request.user.is_authenticated else 'مهمان'
        full_name = f"{first_name} {last_name}"

        today_jalali = jdatetime.date.today().strftime('%Y/%m/%d')

        return Response({
            'experiment_id': experiment.id,
            'full_name': full_name,
            'date': today_jalali,
            'laboratory': laboratory.name,
        })
    
    def post(self, request, pk=None):
        try:
            serializer = RequestInfoSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def patch(self, request, pk=None):
        try:
            instance = RequestInfo.objects.get(pk=pk)
        except RequestInfo.DoesNotExist:
            return Response({'message': 'RequestInfo not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = RequestInfoSerializer(instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    