from django.shortcuts import render
from django.views import View
from django.utils import timezone
from django.views.generic import ListView
from .models import *
from django.views.generic import DetailView
from services.models import Experiment



class DevicesListView(ListView):
    model = Device
    template_name = 'devices/device-home.html'
    context_object_name = 'devices'
    paginate_by = 6

    def get_queryset(self):
        queryset = Device.objects.filter(status='ready',)

        username = self.kwargs.get('username')
        if username:
            queryset = queryset.filter(author__username=username)

        tag_name = self.kwargs.get('tag_name')
        if tag_name:
            queryset = queryset.filter(tags__name=tag_name)

        return queryset

class DevicesDetailView(DetailView):
    model = Device
    template_name = 'devices/device-single.html'
    context_object_name = 'device'

class DevicesExperimentListView(ListView):
    model = Experiment
    template_name = 'devices/device-experiments.html'
    context_object_name = 'experiments'

    def get_queryset(self):
        device_id = self.kwargs['device_id']
        return Experiment.objects.filter(device_id=device_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        device_id = self.kwargs['device_id']
        context['experiments'] = Experiment.objects.filter(device_id=device_id)
        context['device'] = Device.objects.get(id=device_id)
        return context
    
class DevicesSearchView(ListView):
    model = Device
    template_name = 'devices/devices_home.html'
    context_object_name = 'devices'
    paginate_by = 10
    def get_queryset(self):

        query = self.request.GET.get('s')  # Retrieve the 's' parameter from the GET request

        queryset = super().get_queryset().filter(status=1)  # Filter posts by status

        if query:
            # Use 'icontains' for case-insensitive search in both title and content
            queryset = queryset.filter(title__icontains=query) | queryset.filter(content__icontains=query)

        return queryset