from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
import jdatetime
from django.views.generic.edit import FormView
from .forms import TestSearchForm
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView
from django.db.models import Q
from .models import Experiment

class ServicesAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk=None):
        try:
            experiment = Experiment.objects.get(id=pk)
            samples = experiment.samples.all()
            laboratory = experiment.laboratory
        except Experiment.DoesNotExist:
            return Response({
                'full_name': 'مهمان',
                'date': jdatetime.date.today().strftime('%Y/%m/%d'),
                'experiment_id': 'unknown',
                'request_type': 'unknown',
                'sample_types': []
            })

        samples_data = []

        for sample in samples:
            tests = sample.tests.all()
            tests_list = []
            for test in tests:
                standards = test.standards.all()
                standards_data = []
                for standard in standards:
                    parameters = standard.parameters.all()
                    parameters_data = []
                    for parameter in parameters:
                        unit_amount = {
                            'id': parameter.unit_amount.id,
                            'amount': parameter.unit_amount.amount,
                            'unit': parameter.unit_amount.unit,
                            'unit_display': parameter.unit_amount.get_unit_display()
                        }
                        unit_price = {
                            'id': parameter.unit_price.id,
                            'unit_price': str(parameter.unit_price.unit_price),
                            'currency': parameter.unit_price.currency,
                            'currency_display': parameter.unit_price.get_currency_display()
                        }
                        parameters_data.append({
                            'id': parameter.id,
                            'name': parameter.name,
                            'unit': parameter.unit,
                            'unit_display': parameter.get_unit_display(),
                            'laboratory': parameter.laboratory.id,
                            'unit_amount': unit_amount,
                            'unit_price': unit_price
                        })
                    standards_data.append({
                        'standard_id': standard.id,
                        'name': standard.name,
                        'description': standard.description,
                        'parameters': parameters_data
                    })
                
                tests_list.append({
                    'test_id': test.id,
                    'name_fa': test.name_fa,
                    'name_en': test.name_en,
                    'unit_type': test.unit_type,
                    'operating_range': test.operating_range,
                    'description': test.description,
                    'standards': standards_data
                })

            samples_data.append({
                'id': sample.id,
                'name': sample.name,
                'description': sample.description,
                'tests': tests_list  # Including detailed test information here
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
            'laboratory': laboratory.name,
            'sample_types': samples_data  # Now includes the detailed tests data
        })

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