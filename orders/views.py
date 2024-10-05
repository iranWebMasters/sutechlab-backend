from django.views.generic import CreateView
import logging
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import RequestInfo, Experiment,SampleInfo
from django.views.generic import FormView,DetailView,UpdateView,DeleteView
from django.shortcuts import get_object_or_404
import jdatetime
from .forms import *
logger = logging.getLogger(__name__)

class RequestInfoCreateView(LoginRequiredMixin, CreateView):
    model = RequestInfo
    form_class = RequestInfoForm
    template_name = 'requests/request-information.html' 
    success_url = reverse_lazy('orders:sample_info_create')
    
    def get_success_url(self):
        experiment_id = self.kwargs['pk']
        return reverse_lazy('orders:sample_info_create', kwargs={'experiment_id': experiment_id})

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        experiment_id = self.kwargs['pk']
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
        experiment_id = self.kwargs['pk']
        request_info.experiment = get_object_or_404(Experiment, id=experiment_id)
        request_info.user = self.request.user
        request_info.save()
        return super().form_valid(form)

class RequestInfoUpdateView(LoginRequiredMixin, UpdateView):
    model = RequestInfo
    form_class = RequestInfoUpdateForm
    template_name = 'requests/update-request-information.html' 
    context_object_name = 'request_info'
    def form_valid(self, form):
        logger.info(f"Form is valid. Description: {form.cleaned_data.get('description')}")
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.error(f"Form is invalid. Errors: {form.errors}")
        return super().form_invalid(form)

    def get_success_url(self):
        experiment_id = self.kwargs['pk']
        return reverse_lazy('orders:sample_info_create', kwargs={'experiment_id': experiment_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        experiment = self.object.experiment
        
        profile = self.request.user.profile
        full_name = f"{profile.first_name} {profile.last_name}"

        context['experiment'] = experiment
        context['full_name'] = full_name
        context['description'] = self.object.description  # Current description for editing
        context['laboratory_name'] = experiment.laboratory.name  # Name of the associated laboratory
        context['jalali_date'] = jdatetime.datetime.now().strftime('%Y/%m/%d')  # Jalali date
        
        return context


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
        return reverse_lazy('orders:sample_list')  # در صورت عدم وجود experiment_id به صفحه لیست برگردید

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sample'] = self.object  # برای نمایش اطلاعات نمونه در قالب
        return context
    
class TestInformationView(FormView):
    template_name = 'requests/test-information.html'
    def get_context_data(self, **kwargs):
        experiment_id = self.kwargs['experiment_id']
        experiment = get_object_or_404(Experiment,id = experiment_id)
        tests = experiment.tests.all()
        context = {
            'tests': tests,
            'experiment': experiment,
        }
        return context