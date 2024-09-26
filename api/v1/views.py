from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from orders.models import TemporaryRequest
from .serializers import TemporaryRequestSerializer

class TemporaryRequestViewSet(viewsets.ModelViewSet):
    queryset = TemporaryRequest.objects.all()
    serializer_class = TemporaryRequestSerializer

    # ذخیره اطلاعات پایه
    @action(detail=False, methods=['post'])
    def save_basic_info(self, request):
        user = request.user.profile  # فرض می‌کنیم که کاربر لاگین شده است
        description = request.data.get('description')

        temp_request, created = TemporaryRequest.objects.get_or_create(user=user, finalized=False)
        temp_request.description = description
        temp_request.step = 1
        temp_request.save()

        return Response({'message': 'Basic info saved successfully', 'step': temp_request.step})

    # ذخیره اطلاعات نمونه
    @action(detail=False, methods=['post'])
    def save_sample_info(self, request):
        user = request.user.profile
        sample_info = request.data.get('sample_info')

        temp_request = TemporaryRequest.objects.get(user=user, finalized=False)
        temp_request.sample_info = sample_info
        temp_request.step = 2
        temp_request.save()

        return Response({'message': 'Sample info saved successfully', 'step': temp_request.step})

    # ذخیره اطلاعات آزمایش
    @action(detail=False, methods=['post'])
    def save_experiment_info(self, request):
        user = request.user.profile
        experiment_info = request.data.get('experiment_info')

        temp_request = TemporaryRequest.objects.get(user=user, finalized=False)
        temp_request.experiment_info = experiment_info
        temp_request.step = 3
        temp_request.save()

        return Response({'message': 'Experiment info saved successfully', 'step': temp_request.step})

    # نهایی‌سازی درخواست
    @action(detail=False, methods=['post'])
    def finalize_request(self, request):
        user = request.user.profile
        temp_request = TemporaryRequest.objects.get(user=user, finalized=False)

        # انتقال داده‌ها به مدل اصلی
        sample_info_data = temp_request.sample_info
        experiment_info_data = temp_request.experiment_info

        # فرض می‌کنیم که مدل‌های SampleInfo و ExperimentInfo از قبل وجود دارند
        from .models import Request, SampleInfo, ExperimentInfo

        sample_info = SampleInfo.objects.create(**sample_info_data)
        experiment_info = ExperimentInfo.objects.create(**experiment_info_data)

        new_request = Request.objects.create(
            RequestInfo=None,  # پر کردن با اطلاعات RequestInfo
            SampleInfo=sample_info,
            ExperimentInfo=experiment_info,
        )

        temp_request.finalized = True
        temp_request.save()

        return Response({'message': 'Request finalized successfully', 'request_id': new_request.id})
































# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from services.models import *
# from orders.models import *
# from .serializers import *
# import jdatetime
# from rest_framework import status

# class StepOneAPI(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request, pk=None):
#         try:
#             experiment = Experiment.objects.get(id=pk)
#             laboratory = experiment.laboratory
#         except Experiment.DoesNotExist:
#             return Response({'message': 'This experiment is not available'})

#         first_name = request.user.profile.first_name if request.user.is_authenticated else 'مهمان'
#         last_name = request.user.profile.last_name if request.user.is_authenticated else 'مهمان'
#         full_name = f"{first_name} {last_name}"

#         today_jalali = jdatetime.date.today().strftime('%Y/%m/%d')
#         try:
#             request_info = RequestInfo.objects.get(user=request.user.profile, experiment=experiment)
#             description = request_info.description
#         except RequestInfo.DoesNotExist:
#             description = None

#         return Response({
#             'experiment_id': experiment.id,
#             'full_name': full_name,
#             'date': today_jalali,
#             'laboratory': laboratory.name,
#             'description': description,
#         })
    
#     def post(self, request, pk=None):
#         try:
#             experiment = Experiment.objects.get(id=pk)
#             request_data = request.data.copy()
#             request_data['experiment'] = experiment.id

#             serializer = RequestInfoSerializer(data=request_data, context={'request': request})
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Experiment.DoesNotExist:
#             return Response({'error': 'Experiment not found.'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#     def patch(self, request, pk=None):
#         try:
#             experiment_instance = Experiment.objects.get(pk=pk)
#         except Experiment.DoesNotExist:
#             return Response({'message': 'Experiment not found'}, status=status.HTTP_404_NOT_FOUND)
#         try:
#             request_info_instance = RequestInfo.objects.get(experiment=experiment_instance, user=request.user.profile) 
#         except RequestInfo.DoesNotExist:
#             return Response({'message': 'RequestInfo not found for the given experiment and user'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = RequestInfoSerializer(request_info_instance, data=request.data, partial=True, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class StepTwoAPI(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request, pk=None):
#         try:
#             # پیدا کردن آزمایش با ID مشخص
#             experiment = Experiment.objects.prefetch_related('samples').get(id=pk)
            
#             # بارگذاری نمونه‌ها
#             samples = experiment.samples.all()
#             serializer = SampleSerializer(samples, many=True)

#             # پیدا کردن SampleInfo مرتبط با کاربر و آزمایش
#             sampleinfo = SampleInfo.objects.get(user=request.user.profile, experiment=experiment)
#             sampleinfo_serializer = SampleInfoSerializer(sampleinfo)

#             # ترکیب داده‌ها
#             return Response({
#                 'samples': serializer.data,
#                 'sample_info': sampleinfo_serializer.data
#             }, status=status.HTTP_200_OK)

#         except Experiment.DoesNotExist:
#             return Response({"detail": "Experiment not found."}, status=status.HTTP_404_NOT_FOUND)
#         except SampleInfo.DoesNotExist:
#             return Response({"detail": "SampleInfo not found."}, status=status.HTTP_404_NOT_FOUND)

#     def post(self, request, *args, **kwargs):
#         data = request.data
#         return Response(data, status=status.HTTP_201_CREATED)

#     def put(self, request, *args, **kwargs):
#         data = request.data
#         return Response(data, status=status.HTTP_200_OK)

#     def delete(self, request, *args, **kwargs):
#         return Response({"message": "حذف با موفقیت انجام شد"}, status=status.HTTP_204_NO_CONTENT)