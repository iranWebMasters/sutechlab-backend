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
from django.views.generic import ListView, DetailView, DeleteView
from services.models import Experiment
from orders.models import Order
from gateway.models import Payment 
from azbankgateways import models as bank_models
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings
import uuid

from .forms import *

class IndexView(TemplateView):
    template_name = 'userpanel/index.html'
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
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
            context['requests'] = Order.objects.filter(user=self.request.user)
        return context
    

class ProfileUpdatePanelView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdatePanelForm
    template_name = 'userpanel/user-information.html'
    success_url = reverse_lazy('userpanel:index')
    context_object_name = 'profile'
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, "پروفایل شما با موفقیت بروز رسانی شد.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "خطایی در بروز رسانی پروفایل شما رخ داد.")
        response = super().form_invalid(form)
        return response
    
@method_decorator(cache_page(settings.CACHE_TIMEOUT), name='dispatch')
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
@method_decorator(cache_page(settings.CACHE_TIMEOUT), name='dispatch')
class ExperimentDetailView(DetailView):
    model = Experiment
    context_object_name = 'experiment'
    template_name = 'services/experiment-details.html'

    def get_queryset(self):
        return Experiment.objects.prefetch_related('tests', 'samples').select_related('laboratory')

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        profile = Profile.objects.select_related('user').get(user=request.user)
        required_fields = [profile.first_name, profile.last_name, profile.national_id, 
                           profile.phone_number, profile.address, profile.postal_code]
        if not all(required_fields):
            return redirect('update_profile')
        self.profile = profile
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        return context
    

class DownloadInvoiceView(View):
    def get(self, request, request_id):
        try:
            request_instance = Order.objects.get(id=request_id)
            if not request_instance.invoice_pdf:
                return HttpResponse("فاکتور موجود نیست.", status=404)

            response = HttpResponse(
                request_instance.invoice_pdf.read(),
                content_type='application/pdf'
            )
            response['Content-Disposition'] = f'attachment; filename="{request_instance.invoice_pdf.name}"'
            return response

        except Order.DoesNotExist:
            raise Http404("درخواست مربوط به فاکتور پیدا نشد.")

class LaboratoryRequestDeleteView(DeleteView):
    model = Order
    template_name = 'userpanel/order_confirm_delete.html'
    success_url = reverse_lazy('userpanel:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.object
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, "درخواست با موفقیت حذف شد.")
        return HttpResponseRedirect(self.get_success_url())

class RequestEditView(UpdateView):
    model = TemporaryOrder
    form_class = RequestUpdateForm
    template_name = 'userpanel/request_form.html'
    success_url = reverse_lazy('userpanel:index')

    def form_valid(self, form):
        return super().form_valid(form)
    

class LaboratoryRequestDetailView(DetailView):
    model = Order
    template_name = 'userpanel/order_detail.html'

    def get_object(self, queryset=None):
        request_id = self.kwargs.get('pk')
        return get_object_or_404(Order, pk=request_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context['experiment'] = order.experiment
        context['user'] = order.user
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context
    
class PaymentPageView(DetailView):
    model = Order
    template_name = 'userpanel/payment_page.html'

    def get_object(self, queryset=None):
        request_id = self.kwargs.get('request_id')
        return get_object_or_404(Order, id=request_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context
    

class ProcessPaymentView(View):
    def post(self, request, request_id):
        order = get_object_or_404(Order, id=request_id)
        final_amount = order.final_price
        use_wallet = request.POST.get('use_wallet') == 'true'
        amount_to_process = final_amount

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

        tracking_code = str(uuid.uuid4())[:12].replace('-', '').upper()

        if amount_to_process == 0:
            payment = Payment.objects.create(
                order=order,
                user=request.user,
                amount=amount_to_process,
                status='completed',
                tracking_code=tracking_code
            )
            order.status = 'successful'
            order.tracking_code = tracking_code
            order.save()

            messages.success(request, 'پرداخت با موفقیت از طریق کیف پول انجام شد.')
            return redirect('userpanel:payment_success', tracking_code=tracking_code)

        payment = Payment.objects.create(
            order=order,
            user=request.user,
            amount=amount_to_process,
        )
        return redirect('gateway:payment', payment_id=payment.id)

class PaymentSuccessView(DetailView):
    model = Payment
    template_name = 'userpanel/payment_success.html'
    context_object_name = 'payment'
    slug_field = 'tracking_code'
    slug_url_kwarg = 'tracking_code'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payment = self.get_object()
        context['tracking_code'] = payment.tracking_code
        context['amount'] = payment.amount
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context