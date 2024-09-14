from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
import jdatetime
from django.views.generic.edit import FormView
from .forms import TestSearchForm
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

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
            'sample_types': SampleSerializer(samples, many=True).data,
            'tests': tests_data
            
        })

# views.py

from django.views.generic import ListView
from django.db.models import Q
from .models import Experiment
from .forms import TestSearchForm

class TestSearchView(ListView):
    model = Experiment
    template_name = 'services/search_results.html'  # نام الگو
    context_object_name = 'results'  # نام متغیر نتایج در الگو
    form_class = TestSearchForm

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.form_class(self.request.GET)

        if form.is_valid():
            test_name = form.cleaned_data.get('test_name')
            laboratory_name = form.cleaned_data.get('laboratory_name')
            faculty_name = form.cleaned_data.get('faculty_name')

            # جستجو بر اساس فیلدهای مختلف
            filters = Q()
            if test_name:
                filters |= Q(test_name__icontains=test_name)
            if laboratory_name:
                filters |= Q(laboratory__name__icontains=laboratory_name)
            if faculty_name:
                filters |= Q(laboratory__faculty__name__icontains=faculty_name)

            queryset = queryset.filter(filters)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile  # اضافه کردن فرم به context
        return context

class AutocompleteTestsView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        results = []

        if query:
            tests = Tests.objects.filter(name_fa__icontains=query)[:10]  # محدود کردن به 10 نتیجه
            for test in tests:
                results.append({
                    'test_name': test.name_fa,
                    'laboratory_name': test.laboratory.name,
                    'faculty_name': test.laboratory.faculty.name,
                })

        return JsonResponse(results, safe=False)