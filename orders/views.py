from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import RequestInfo, Experiment,SampleInfo,TestInfo
from django.views.generic import FormView,DetailView,UpdateView,DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse
from services.models import Test
from django.views import View
import logging
import jdatetime

from .forms import *


logger = logging.getLogger(__name__)

class RequestInfoCreateView(LoginRequiredMixin, CreateView):
    model = RequestInfo
    form_class = RequestInfoForm
    template_name = 'requests/request-information.html' 
    success_url = reverse_lazy('orders:sample_info_create')
    
    def get_success_url(self):
        experiment_id = self.kwargs['experiment_id']
        return reverse_lazy('orders:sample_info_create', kwargs={'experiment_id': experiment_id})

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        experiment_id = self.kwargs['experiment_id']
        experiment = get_object_or_404(Experiment, id=experiment_id)
        
        jalali_date = jdatetime.datetime.now().strftime('%Y/%m/%d')

        profile=self.request.user.profile
        full_name = profile.first_name +" " +profile.last_name
        context['full_name'] = full_name
        context['jalali_date'] = jalali_date
        context['experiment'] = experiment
        context['laboratory_name'] = experiment.laboratory.name
        
        return context

    def form_valid(self, form):
        request_info = form.save(commit=False)
        experiment_id = self.kwargs['experiment_id']
        request_info.experiment = get_object_or_404(Experiment, id=experiment_id)
        request_info.user = self.request.user
        request_info.save()
        return super().form_valid(form)


class SampleInfoCreateView(FormView):
    template_name = 'requests/sample-information.html'
    form_class = SampleForm

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        experiment_id = self.kwargs.get('experiment_id')
        experiment = get_object_or_404(Experiment, id=experiment_id)
        current_user = self.request.user
        user_samples = SampleInfo.objects.filter(experiment=experiment, user=current_user)

        context['user_samples'] = user_samples 
        context['samples'] = experiment.samples.all()
        context['experiment'] = experiment
        context['formset'] = self.get_form()
        return context
        
    def form_valid(self, form):
        request_info = form.save(commit=False)
        experiment_id = self.kwargs['experiment_id']
        request_info.experiment = get_object_or_404(Experiment, id=experiment_id)
        request_info.user = self.request.user
        request_info.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        logger.error("Form is invalid.")
        logger.error(form.errors)  # Log the form errors
        return super().form_invalid(form)
    
class SampleDetailView(DetailView):
    model = SampleInfo
    template_name = 'requests/sample_detail.html'
    context_object_name = 'sample'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # هر داده اضافی که نیاز دارید را می‌توانید به context اضافه کنید
        return context

class SampleEditView(UpdateView):
    model = SampleInfo
    form_class = SampleForm
    # template_name = 'requests/sample_edit.html'
    template_name = 'requests/sample-information.html'
    context_object_name = 'sample'

    def get_success_url(self):
        return self.request.path  # به همان صفحه برمی‌گردد
    
class SampleDeleteView(DeleteView):
    model = SampleInfo
    template_name = 'requests/sample_confirm_delete.html'
    
    def get_success_url(self):
        # اطمینان از وجود experiment_id در kwargs
        experiment_id = self.kwargs.get('experiment_id')
        if experiment_id:
            return reverse_lazy('orders:sample_info_create', kwargs={'experiment_id': experiment_id})
        return reverse_lazy('orders:sample_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sample'] = self.object  # برای نمایش اطلاعات نمونه در قالب
        return context
    
class TestInfoCreateView(FormView):
    template_name = 'requests/test-information.html'
    form_class = TestInfoForm

    def get_success_url(self):
        return self.request.path
    def get_context_data(self, **kwargs):
        experiment_id = self.kwargs['experiment_id']
        experiment = get_object_or_404(Experiment,id = experiment_id)
        current_user = self.request.user
        user_samples = SampleInfo.objects.filter(experiment=experiment, user=current_user)
        user_tests = TestInfo.objects.filter(experiment=experiment, user=current_user)
        tests = experiment.tests.all()
        context = {
            'tests': tests,
            'experiment': experiment,
            'user_samples': user_samples,
            'user_tests': user_tests,
        }
        return context
    
    def form_valid(self, form):
        request_info = form.save(commit=False)
        experiment_id = self.kwargs['experiment_id']
        request_info.experiment = get_object_or_404(Experiment, id=experiment_id)
        request_info.user = self.request.user
        request_info.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        logger.error("Form is invalid.")
        logger.error(form.errors)  # Log the form errors
        return super().form_invalid(form)

class TestParametersView(View):
    def get(self, request, test_id, *args, **kwargs):
        try:
            test = Test.objects.get(id=test_id)
            parameters = test.parameters.all()
            parameters_data = [{'id': param.id, 'name': param.name} for param in parameters]
            return JsonResponse({'parameters': parameters_data})
        except Test.DoesNotExist:
            return JsonResponse({'error': 'Test not found'}, status=404)
        
class TestDetailView(DetailView):
    model = TestInfo
    template_name = 'orders/test_detail.html'
    context_object_name = 'test'

    def get_object(self):
        test_id = self.kwargs.get('pk')
        return get_object_or_404(TestInfo, id=test_id)
    
class TestUpdateView(UpdateView):
    model = TestInfo
    form_class = TestInfoForm
    template_name = 'requests/test_edit.html'
    context_object_name = 'test'
    def get_success_url(self):
        experiment_id = self.kwargs['experiment_id']
        return reverse_lazy('orders:test_info_create',  kwargs={'experiment_id': experiment_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        experiment_id = self.kwargs['experiment_id']
        test_pk = self.kwargs['pk']
        experiment = get_object_or_404(Experiment, id=experiment_id)
        current_user = self.request.user
        
        user_samples = SampleInfo.objects.filter(experiment=experiment, user=current_user)
        
        user_test = get_object_or_404(TestInfo, experiment=experiment, user=current_user, pk=test_pk)
        
        tests = experiment.tests.all()
        
        context.update({
            'tests': tests,
            'experiment': experiment,
            'user_samples': user_samples,
            'user_test': user_test,
        })
        
        return context


class TestDeleteView(DeleteView):
    model = TestInfo
    template_name = 'requests/test-information.html'
    context_object_name = 'test'

    def get_success_url(self):
        experiment_id = self.kwargs.get('experiment_id')
        if experiment_id:
            return reverse_lazy('orders:test_info_create', kwargs={'experiment_id': experiment_id})
        return reverse_lazy('orders:sample_list')

class DiscountInfoFormView(FormView):
    form_class = DiscountInfoForm
    template_name = 'requsets/discount_info.html'

    def form_valid(self, form):
        request_info = form.save(commit=False)
        experiment_id = self.kwargs['experiment_id']
        request_info.experiment = get_object_or_404(Experiment, id=experiment_id)
        request_info.user = self.request.user
        request_info.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        logger.error("Form is invalid.")
        logger.error(form.errors)  # Log the form errors
        return super().form_invalid(form)