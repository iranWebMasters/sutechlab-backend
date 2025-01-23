from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import  Experiment,SampleInfo,TestInfo,Parameters
from django.views.generic import FormView,DetailView,UpdateView,DeleteView
from django.shortcuts import get_object_or_404,redirect,render
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from services.models import Test
from django.views import View
from accounts.models import Profile
from accounts.models import User
import logging
import jdatetime
import json
from .forms import *

class MultiStepOrderView(LoginRequiredMixin, View):
    order = None

    def dispatch(self, request, *args, **kwargs):
        self.order = Order.objects.filter(user=request.user, is_complete=False).first()
        if self.order:
            if self.order.current_step < self.get_step_number():
                return redirect(self.get_redirect_url())
        return super().dispatch(request, *args, **kwargs)

    def get_step_number(self):
        """مرحله جاری (override در ویوهای فرزند)"""
        raise NotImplementedError("You must implement get_step_number.")

    def get_redirect_url(self):
        """URL مرحله‌ای که باید به آن هدایت شود (override در ویوهای فرزند)"""
        raise NotImplementedError("You must implement get_redirect_url.")

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/request-information.html' 
    success_url = reverse_lazy('orders:sample_info_create')

    def get_success_url(self):
        return reverse_lazy('orders:sample_info_create', kwargs={'order_code': self.object.order_code})

        
    def get_step_number(self):
        return 2

    def get_redirect_url(self):
        return reverse('orders:sample_info_create', kwargs={'order_code': self.order.order_code})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        experiment_id = self.kwargs['experiment_id']
        experiment = get_object_or_404(Experiment, id=experiment_id)

        profile = self.request.user.profile
        context.update({
            'jalali_date': jdatetime.datetime.now().strftime('%Y/%m/%d'),
            'experiment': experiment,
            'laboratory_name': experiment.laboratory.name,
            'profile': profile,
            'current_step': 1,
        })
        return context

    def form_valid(self, form):
        order = form.save(commit=False)
        experiment_id = self.kwargs['experiment_id']
        order.experiment = get_object_or_404(Experiment, id=experiment_id)
        order.user = self.request.user
        order.save()
        self.request.session['order_code'] = order.order_code
        return super().form_valid(form)


class SampleInfoCreateView(FormView):
    template_name = 'orders/sample-information.html'
    form_class = SampleForm
    order = None

    def dispatch(self, request, *args, **kwargs):
        order_code = self.kwargs.get('order_code')
        self.order = get_object_or_404(Order, order_code=order_code)
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return self.request.path
    
    def get_step_number(self):
        return 2

    def get_redirect_url(self):
        return reverse('orders:sample_info_create', kwargs={'order_code': self.order.order_code})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        experiment = self.order.experiment
        context.update({
            'order': self.order,
            'user_samples': SampleInfo.objects.filter(order=self.order),
            'profile': self.request.user.profile,
            'samples': experiment.samples.all(),
            'experiment': experiment,
            'current_step': 2,
        })
        return context
        
    def form_valid(self, form):
        sample_info = form.save(commit=False)
        sample_info.order = self.order
        sample_info.save()
        self.order.current_step = self.get_step_number() + 1
        self.order.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "لطفا تمام فیلد ها را پر کنید.")
        
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")

        return super().form_invalid(form)
    
class SampleDetailView(DetailView):
    model = SampleInfo
    template_name = 'orders/sample_detail.html'
    context_object_name = 'sample'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile         
        # هر داده اضافی که نیاز دارید را می‌توانید به context اضافه کنید
        return context

class SampleEditView(UpdateView):
    model = SampleInfo
    form_class = SampleForm
    # template_name = 'orders/sample_edit.html'
    template_name = 'orders/sample-information.html'
    context_object_name = 'sample'

    def get_success_url(self):
        return self.request.path  # به همان صفحه برمی‌گردد
    
class SampleDeleteView(DeleteView):
    model = SampleInfo
    template_name = 'orders/sample_confirm_delete.html'
    
    def get_success_url(self):
        order_code = self.kwargs.get('order_code')
        return reverse_lazy('orders:sample_info_create', kwargs={'order_code': order_code})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sample'] = self.object
        return context
    
class TestInfoCreateView(FormView):
    template_name = 'orders/test-information.html'
    form_class = TestInfoForm
    order = None


    def dispatch(self, request, *args, **kwargs):
        order_code = self.kwargs.get('order_code')
        self.order = get_object_or_404(Order, order_code=order_code)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.path
    
    def get_step_number(self):
        return 3

    def get_redirect_url(self):
        return reverse('orders:test_info_create', kwargs={'order_code': self.order.order_code})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        experiment = self.order.experiment
        context.update({
            'order': self.order,
            'profile': self.request.user.profile,
            'experiment': experiment,
            'user_samples': SampleInfo.objects.filter(order=self.order),
            'user_tests': TestInfo.objects.filter(order=self.order),
            'tests': experiment.tests.all(),
            'current_step': 3,
        })
        return context
    
    def form_valid(self, form):
        test_info = form.save(commit=False)
        test_info.order = self.order

        parameter_values = {}
        for key, value in self.request.POST.items():
            if key not in form.cleaned_data:
                parameter_values[key] = value

        if 'csrfmiddlewaretoken' in parameter_values:
            del parameter_values['csrfmiddlewaretoken']

        print("Collected parameter values without CSRF token:", parameter_values)
        test_info.parameter_values = json.dumps(parameter_values)
        print("JSON parameter values to be saved:", test_info.parameter_values)
        test_info.save()
        self.order.current_step = self.get_step_number() + 1
        self.order.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "فرم نامعتبر است.")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

class TestParametersView(View):
    def get(self, request, test_id, *args, **kwargs):
        try:
            test = Test.objects.get(id=test_id)
            parameters = test.parameters.all()
            parameters_data = [{'id': param.id, 'name': param.name} for param in parameters]
            return JsonResponse({'parameters': parameters_data})
        except Test.DoesNotExist:
            return JsonResponse({'error': 'Test not found'}, status=404)

class ParameterValuesView(View):
    def get(self,request,parameter_id,*args,**kwargs):
        try:
            parameter = Parameters.objects.get(id=parameter_id)
            values = parameter.values.all()
            values_data = [
                {
                    'id':value.id,
                    'name':value.name,
                    'default_value':value.default_value,
                    'min_value':value.min_value,
                    'max_value':value.max_value
                    }
                    for value in values]
            return JsonResponse({'values':values_data})
        except Parameters.DoesNotExist:
            return JsonResponse({'error': 'Parameter not found'},status=404)
        
class TestDetailView(DetailView):
    model = TestInfo
    template_name = 'orders/test_detail.html'
    context_object_name = 'test'

    def get_object(self):
        test_id = self.kwargs.get('pk')
        return get_object_or_404(TestInfo, id=test_id)
    
class TestUpdateView(UpdateView):
    model = TestInfo
    form_class = TestInfoForm
    template_name = 'orders/test_edit.html'
    context_object_name = 'test'
    def get_success_url(self):
        experiment_id = self.kwargs['experiment_id']
        return reverse_lazy('orders:test_info_create',  kwargs={'experiment_id': experiment_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        experiment_id = self.kwargs['experiment_id']
        test_pk = self.kwargs['pk']
        experiment = get_object_or_404(Experiment, id=experiment_id)
        current_user = self.request.user
        
        user_samples = SampleInfo.objects.filter(experiment=experiment, user=current_user)
        
        user_test = get_object_or_404(TestInfo, experiment=experiment, user=current_user, pk=test_pk)
        
        tests = experiment.tests.all()
        
        context.update({
            'tests': tests,
            'experiment': experiment,
            'user_samples': user_samples,
            'user_test': user_test,
        })
        
        return context


class TestDeleteView(DeleteView):
    model = TestInfo
    template_name = 'orders/test-information.html'
    context_object_name = 'test'

    def get_success_url(self):
        experiment_id = self.kwargs.get('experiment_id')
        if experiment_id:
            return reverse_lazy('orders:test_info_create', kwargs={'experiment_id': experiment_id})
        return reverse_lazy('orders:sample_list')

class DiscountInfoFormView(FormView):
    form_class = DiscountInfoForm
    template_name = 'orders/discount_info.html'
    order = None

    def dispatch(self, request, *args, **kwargs):
        order_code = self.kwargs.get('order_code')
        self.order = get_object_or_404(Order, order_code=order_code)
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('userpanel:index')
    
    def get_step_number(self):
        return 4

    def get_redirect_url(self):
        return reverse('orders:discount_info', kwargs={'order_code': self.order.order_code})
    
    def form_valid(self, form):
        discount_info = form.save(commit=False)
        discount_info.order = self.order
        discount_info.save()
        self.order.is_complete = True
        self.order.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "فرم نامعتبر است.")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'order': self.order,
            'profile': self.request.user.profile,
            'current_step': 4,
        })
        return context

class UserOrderCancelView(View):
    template_name = 'userpanel/order_confirm_cancel.html'
    success_url = reverse_lazy('userpanel:experiments-list')

    def get(self, request, order_code):
        order = get_object_or_404(Order, order_code=order_code)
        profile = Profile.objects.get(user=request.user)
        referer = request.META.get('HTTP_REFERER', reverse('userpanel:index'))
        return render(request, self.template_name, {
            'order': order,
            'profile': profile,
            'referer': referer
        })

    def post(self, request, order_code):
        order = get_object_or_404(Order, order_code=order_code)
        SampleInfo.objects.filter(order=order).delete()
        TestInfo.objects.filter(order=order).delete()
        DiscountInfo.objects.filter(order=order).delete()
        order.delete()
        return redirect(self.success_url)