from .models import *
from .forms import TestSearchForm
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView
from django.db.models import Q
from .models import Experiment

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