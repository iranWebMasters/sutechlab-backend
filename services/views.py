from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
import jdatetime

class ServicesAPI(APIView):
    permission_classes = [IsAuthenticated] 
    
    def get(self, request, pk=None):
        try:
            experiment = Experiment.objects.get(id=pk)
            tests = experiment.tests.all()
            samples = Sample.objects.filter(experiments__id=pk)
            laboratory  = Laboratory.objects.filter(experiments__id=pk)
        except Experiment.DoesNotExist:
            return Response({
                'username': 'مهمان',
                'date_jalali': jdatetime.date.today().strftime('%Y/%m/%d'),
                'service_id': request.query_params.get('service_id', 'unknown'),
                'request_type': 'unknown',
                'experiments': [],
                'standards': [],
                'samples': []
            })

        tests_data = []

        for test in tests:
            standards = test.standards.all()
            standards_data = []
            for standard in standards:
                parameters = standard.parameters.all()
                parameters_serializer = ParametersSerializer(parameters, many=True)
                standards_data.append({
                    'standard_id': standard.id,
                    'name': standard.name,
                    'description': standard.description,
                    'parameters': parameters_serializer.data
                })

            tests_data.append({
                'test_id': test.id,
                'name_fa': test.name_fa,
                'name_en': test.name_en,
                'unit_type': test.unit_type,
                'operating_range': test.operating_range,
                'description': test.description,
                'standards': standards_data
            })

        first_name = request.user.profile.first_name if request.user.is_authenticated else 'مهمان'
        last_name = request.user.profile.last_name if request.user.is_authenticated else 'مهمان'
        full_name = f"{first_name} {last_name}"

        today_jalali = jdatetime.date.today().strftime('%Y/%m/%d')


        return Response({
            'full_name': full_name,
            'date': today_jalali,
            'request_type': experiment.request_type,
            'experiment_id': experiment.id,
            'laboratory':LaboratorySerializer(laboratory,many=True).data,
            'samples': SampleSerializer(samples, many=True).data,
            'tests': tests_data
            
        })
