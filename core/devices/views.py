from django.shortcuts import render
from django.views import View
from django.utils import timezone
from django.views.generic import ListView
from .models import *
from django.views.generic import DetailView



class DevicesListView(ListView):
    model = Device
    template_name = 'devices/device-home.html'
    context_object_name = 'devices'
    paginate_by = 6

    def get_queryset(self):
        queryset = Device.objects.filter(status=True,)

        username = self.kwargs.get('username')
        if username:
            queryset = queryset.filter(author__username=username)

        tag_name = self.kwargs.get('tag_name')
        if tag_name:
            queryset = queryset.filter(tags__name=tag_name)

        return queryset

class DevicesDetailView(DetailView):
    model = Device
    template_name = 'devices/service-single.html'
    context_object_name = 'devices'


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