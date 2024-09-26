from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .models import *
from services.models import Experiment
import jdatetime


class RequestTemplateView(TemplateView):
    template_name = 'requests/experiment-request.html'

    def get_context_data(self,pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experiment_id'] = self.kwargs.get('pk')
        profile = Profile.objects.get(user=self.request.user)
        today_jalali = jdatetime.date.today().strftime('%Y/%m/%d')

        full_name = profile.first_name + profile.last_name
        experiment = Experiment.objects.prefetch_related('samples').get(id=pk)
        samples = experiment.samples.all()

        context['full_name'] = full_name
        context['today_jalali'] = today_jalali
        context['samples'] = samples
        return context
    
