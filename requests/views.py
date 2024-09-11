from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Request, SampleInfo
from services.models import Experiment


class RequestListView(ListView):
    model = Request
    template_name = 'requests/request_list.html'  
    context_object_name = 'requests' 

class RequestCreateView(CreateView):
    model = Request
    template_name = 'requests/experiment-request.html'
    success_url = reverse_lazy('request-list')  

class RequestDetailView(DetailView):
    model = Experiment
    template_name = 'requests/experiment-request.html'
    context_object_name = 'request'  







# class RequestUpdateView(UpdateView):
#     model = Request
#     template_name = 'requests/request_form.html'
#     success_url = reverse_lazy('request-list')

# class RequestDeleteView(DeleteView):
#     model = Request
#     template_name = 'requests/request_confirm_delete.html'
#     success_url = reverse_lazy('request-list')

# class SampleListView(ListView):
#     model = SampleInfo
#     template_name = 'samples/sample_list.html'
#     context_object_name = 'samples'

# class SampleCreateView(CreateView):
#     model = SampleInfo
#     template_name = 'samples/sample_form.html'
#     success_url = reverse_lazy('sample-list')

# class SampleDetailView(DetailView):
#     model = SampleInfo
#     template_name = 'samples/sample_detail.html'
#     context_object_name = 'sample'

# class SampleUpdateView(UpdateView):
#     model = SampleInfo
#     template_name = 'samples/sample_form.html'
#     success_url = reverse_lazy('sample-list')

# class SampleDeleteView(DeleteView):
#     model = SampleInfo
#     template_name = 'samples/sample_confirm_delete.html'
#     success_url = reverse_lazy('sample-list')

