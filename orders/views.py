from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView,TemplateView
from .models import *
from services.models import Experiment

class RequestTemplateView(TemplateView):
    template_name = 'requests/experiment-request.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experiment_id'] = self.kwargs.get('pk')
        return context
