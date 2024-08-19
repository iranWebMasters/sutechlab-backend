from django.shortcuts import render
from django.views import View
from django.utils import timezone
from django.views.generic import ListView
from .models import *
from django.views.generic import DetailView



class ServicesListView(ListView):
    model = Services
    template_name = 'services/services_home.html'
    context_object_name = 'services'
    paginate_by = 6

    def get_queryset(self):
        current_time = timezone.now()
        queryset = Services.objects.filter(status=True, published_date__lte=current_time).order_by('-published_date')

        cat_name = self.kwargs.get('cat_name')
        if cat_name:
            queryset = queryset.filter(category__name=cat_name)

        username = self.kwargs.get('username')
        if username:
            queryset = queryset.filter(author__username=username)

        tag_name = self.kwargs.get('tag_name')
        if tag_name:
            queryset = queryset.filter(tags__name=tag_name)

        return queryset

class ServicesDetailView(DetailView):
    model = Services
    template_name = 'services/service-single.html'
    context_object_name = 'post'


class ServicesSearchView(ListView):
    model = Services
    template_name = 'services/services_home.html'
    context_object_name = 'services'
    paginate_by = 10
    def get_queryset(self):

        query = self.request.GET.get('s')  # Retrieve the 's' parameter from the GET request

        queryset = super().get_queryset().filter(status=1)  # Filter posts by status

        if query:
            # Use 'icontains' for case-insensitive search in both title and content
            queryset = queryset.filter(title__icontains=query) | queryset.filter(content__icontains=query)

        return queryset