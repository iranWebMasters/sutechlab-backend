from typing import Any
from django.http import HttpRequest
from django.views.generic import TemplateView
from accounts.models import Profile
from django.contrib import messages
from django.db.models.base import Model as Model
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView,DeleteView
from services.models import Experiment
from orders.models import LaboratoryRequest
from django.contrib import messages
from django.http import HttpResponseRedirect,Http404


from .forms import *



class IndexView(TemplateView):
    template_name = 'userpanel/index.html'
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            profile = Profile.objects.get(user = request.user)
            required_fields = [profile.first_name, profile.last_name, profile.national_id, 
                           profile.phone_number, profile.address, profile.postal_code]
            if not all(required_fields):
                return redirect('update_profile')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            context['profile'] = profile
            
            context['requests'] = LaboratoryRequest.objects.filter(user=self.request.user)
        
        return context
    

class ProfileUpdatePanelView(LoginRequiredMixin,UpdateView):
    model = Profile
    form_class = ProfileUpdatePanelForm
    template_name = 'userpanel/user-information.html'
    success_url = reverse_lazy('userpanel:index')
    context_object_name = 'profile'
    
    def get_object(self):
        return Profile.objects.get(user = self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request,"پروفایل شما با موفقیت بروز رسانی شد.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,"خطایی در بروز رسانی پروفایل شما رخ داد.")
        response = super().form_invalid(form)
        return response
    


class ExperimentListView(ListView):
    model = Experiment
    template_name = 'services/experiment-list.html'

    context_object_name = 'experiments'
    ordering = ['-created_date']
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context

class TestDetailView(DetailView):
    model = Experiment
    context_object_name = 'experiments'
    
    template_name = 'services/experiment-details.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context




class DownloadInvoiceView(View):
    def get(self, request, request_id):
        try:
            # Retrieve the LaboratoryRequest instance
            request_instance = LaboratoryRequest.objects.get(id=request_id)

            # Check if the invoice PDF exists
            if not request_instance.invoice_pdf:
                return HttpResponse("فاکتور موجود نیست.", status=404)

            # Create HttpResponse for downloading the PDF file
            response = HttpResponse(
                request_instance.invoice_pdf.read(),
                content_type='application/pdf'
            )
            response['Content-Disposition'] = f'attachment; filename="{request_instance.invoice_pdf.name}"'
            return response

        except LaboratoryRequest.DoesNotExist:
            raise Http404("درخواست مربوط به فاکتور پیدا نشد.")

class LaboratoryRequestDeleteView(DeleteView):
    model = LaboratoryRequest
    template_name = 'userpanel/confirm_delete.html'  # Specify a template for confirmation
    success_url = reverse_lazy('userpanel:index')  # URL to redirect after successful deletion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.object
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile  # Pass the instance to the template for context
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, "درخواست با موفقیت حذف شد.")  # Success message
        return HttpResponseRedirect(self.get_success_url())

class RequestEditView(UpdateView):
    model = Request
    form_class = RequestUpdateForm  # فرم جدید را به اینجا اضافه کنید
    template_name = 'userpanel/request_form.html'
    success_url = reverse_lazy('userpanel:index')  # URL بعد از موفقیت در ویرایش

    def form_valid(self, form):
        # می‌توانید هر کدی که نیاز دارید را اینجا اضافه کنید
        return super().form_valid(form)