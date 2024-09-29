from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import RequestInfo, Experiment
from django.views.generic import FormView
from django.shortcuts import get_object_or_404
from .forms import *

class RequestInfoCreateView(LoginRequiredMixin, CreateView):
    model = RequestInfo
    form_class = RequestInfoForm
    template_name = 'requests/request-information.html'  # تغییر به نام الگوی جدید
    success_url = reverse_lazy('orders:sample_info_create')  # آدرس مرحله بعدی را مشخص کنید
    
    def get_success_url(self):
        experiment_id = self.kwargs['experiment_id']
        return reverse_lazy('orders:sample_info_create', kwargs={'experiment_id': experiment_id})

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        experiment_id = self.kwargs['experiment_id']
        experiment = get_object_or_404(Experiment, id=experiment_id)
        
        profile=self.request.user.profile
        full_name = profile.first_name +" " +profile.last_name
        context['full_name'] = full_name
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
    form_class = SampleInfoForm
    success_url = reverse_lazy('next_step_url')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        experiment_id = self.kwargs.get('experiment_id')
        experiment = get_object_or_404(Experiment, id=experiment_id)
        context['samples'] = experiment.samples.all()
        context['experiment'] = experiment
        context['formset'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        experiment_id = self.kwargs.get('experiment_id')
        experiment = get_object_or_404(Experiment, id=experiment_id)
        
        formset = SampleInfoFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.experiment = experiment  # مرتبط کردن نمونه‌ها به آزمایش
                instance.save()
            return self.form_valid(formset)
        else:
            return self.form_invalid(formset)