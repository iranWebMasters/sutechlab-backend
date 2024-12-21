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
from django.shortcuts import get_object_or_404
from gateway.models import Payment 
from azbankgateways import models as bank_models
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import uuid



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

@method_decorator(login_required, name='dispatch')
class TestDetailView(DetailView):
    model = Experiment
    context_object_name = 'experiments'
    
    template_name = 'services/experiment-details.html'
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            profile = Profile.objects.get(user = request.user)
            required_fields = [profile.first_name, profile.last_name, profile.national_id, 
                           profile.phone_number, profile.address, profile.postal_code]
            if not all(required_fields):
                return redirect('update_profile')
        return super().dispatch(request, *args, **kwargs)

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
    

class LaboratoryRequestDetailView(DetailView):
    model = LaboratoryRequest
    template_name = 'userpanel/laboratory_request_detail.html'  # Specify your template

    def get_object(self, queryset=None):
        # Override to get the object based on the URL parameter
        request_id = self.kwargs.get('pk')
        return get_object_or_404(LaboratoryRequest, pk=request_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        laboratory_request = self.get_object()  # Get the current LaboratoryRequest instance
        
        # Add extra context if needed
        context['experiment'] = laboratory_request.experiment  # Pass the related Experiment object
        context['user'] = laboratory_request.user  # Pass the user who made the request
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        # You can add more context variables as needed
        return context
    

class PaymentPageView(DetailView):
    model = LaboratoryRequest
    template_name = 'userpanel/payment_page.html'  # Create this template for payment

    def get_object(self, queryset=None):
        # Get the object based on the request ID passed in the URL
        request_id = self.kwargs.get('request_id')
        return get_object_or_404(LaboratoryRequest, id=request_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch the profile for the current user
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context
    

class ProcessPaymentView(View):
    def post(self, request, request_id):
        laboratory_request = get_object_or_404(LaboratoryRequest, id=request_id)
        final_amount = laboratory_request.final_price
        use_wallet = request.POST.get('use_wallet') == 'true'
        amount_to_process = final_amount

        # اگر از کیف پول استفاده شود
        if use_wallet:
            profile = get_object_or_404(Profile, user=request.user)
            wallet_balance = profile.wallet_balance

            if wallet_balance >= final_amount:
                amount_to_process = 0
                profile.wallet_balance -= final_amount
            else:
                amount_to_process = final_amount - wallet_balance
                profile.wallet_balance = 0

            profile.save()

        # اگر مبلغ قابل پرداخت صفر باشد، مستقیماً پرداخت را کامل کن
        tracking_code = str(uuid.uuid4())[:12].replace('-', '').upper()

        if amount_to_process == 0:
            payment = Payment.objects.create(
                laboratory_request=laboratory_request,
                user=request.user,
                amount=amount_to_process,
                status='completed',
                tracking_code=tracking_code  # تنظیم کد رهگیری
            )
            laboratory_request.status = 'successful'
            laboratory_request.tracking_code = tracking_code  # ثبت کد رهگیری در درخواست آزمایش
            laboratory_request.save()

            messages.success(request, 'پرداخت با موفقیت از طریق کیف پول انجام شد.')
            return redirect('userpanel:payment_success', tracking_code=tracking_code)

        # در غیر این صورت، فرآیند پرداخت به درگاه ادامه پیدا می‌کند
        payment = Payment.objects.create(
            laboratory_request=laboratory_request,
            user=request.user,
            amount=amount_to_process,
        )
        return redirect('gateway:payment', payment_id=payment.id)

    

class PaymentSuccessView(DetailView):
    model = Payment
    template_name = 'userpanel/payment_success.html'
    context_object_name = 'payment'
    slug_field = 'tracking_code'  # استفاده از tracking_code برای پیدا کردن پرداخت
    slug_url_kwarg = 'tracking_code'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the payment instance from the context
        payment = self.get_object()  # This retrieves the Payment instance based on the slug
        
        # Use the payment instance to populate the context
        context['tracking_code'] = payment.tracking_code
        context['amount'] = payment.amount
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context