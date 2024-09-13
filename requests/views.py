from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import *
from services.models import Experiment
from .forms import *
import jdatetime
from datetime import datetime

class RequestCreateView(CreateView):
    model = Request
    form_class = RequestForm
    template_name = 'requests/test.html'
    success_url = reverse_lazy('userpanel:index')

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            return super().form_invalid(form)

        try:
            profile = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return super().form_invalid(form)

        form.instance.user = profile
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=self.request.user)
                context['full_name'] = f"{profile.first_name} {profile.last_name}"
            except Profile.DoesNotExist:
                context['full_name'] = "نام کاربری"
        from datetime import datetime
        import jdatetime
        current_datetime = datetime.now()
        current_date = jdatetime.date.fromgregorian(date=current_datetime.date())
        context['current_date'] = current_date.strftime('%Y/%m/%d')
        return context

class RequestListView(ListView):
    model = Request
    template_name = 'requests/request_list.html'  
    context_object_name = 'requests' 


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


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if self.request.user.is_authenticated:
    #         try:
    #             profile = Profile.objects.get(user=self.request.user)
    #             context['full_name'] = f"{profile.first_name} {profile.last_name}"
    #         except Profile.DoesNotExist:
    #             context['full_name'] = "نام کاربری"
    #     from datetime import datetime
    #     import jdatetime
    #     current_datetime = datetime.now()
    #     current_date = jdatetime.date.fromgregorian(date=current_datetime.date())
    #     context['current_date'] = current_date.strftime('%Y/%m/%d')
    #     return context