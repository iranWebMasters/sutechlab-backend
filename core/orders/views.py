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

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/request-information.html' 
    success_url = reverse_lazy('orders:sample_info_create')
    
    def get_success_url(self):
        return reverse_lazy('orders:sample_info_create', kwargs={'order_code': self.object.order_code})

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        experiment_id = self.kwargs['experiment_id']
        experiment = get_object_or_404(Experiment, id=experiment_id)
        
        jalali_date = jdatetime.datetime.now().strftime('%Y/%m/%d')

        profile=self.request.user.profile
        full_name = profile.first_name +" " +profile.last_name
        context['full_name'] = full_name
        context['jalali_date'] = jalali_date
        context['experiment'] = experiment
        context['laboratory_name'] = experiment.laboratory.name
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        context['current_step'] = 1
        
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

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_code = self.kwargs.get('order_code')
        order = get_object_or_404(Order, order_code=order_code)
        experiment = order.experiment
        context['order'] = order
        context['user_samples'] = SampleInfo.objects.filter(order=order)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile 
        context['samples'] = experiment.samples.all()
        context['experiment'] = experiment
        context['formset'] = self.get_form()
        context['current_step'] = 2

        return context
        
    def form_valid(self, form):
        sample_info = form.save(commit=False)
        order_code = self.kwargs.get('order_code')
        order = get_object_or_404(Order, order_code=order_code)
        sample_info.order = order
        sample_info.save()

        return super().form_valid(form)
    
    def form_invalid(self, form):
        logger.error("Form is invalid.")
        logger.error(form.errors)  # Log the form errors
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

    def get_success_url(self):
        return self.request.path
    def get_context_data(self, **kwargs):
        order_code = self.kwargs.get('order_code')
        order = get_object_or_404(Order, order_code=order_code)
        experiment = order.experiment
        user_samples = SampleInfo.objects.filter(order=order)
        user_tests = TestInfo.objects.filter(order=order)
        tests = experiment.tests.all()
        profile = Profile.objects.get(user=self.request.user)
        context = {
            'tests': tests,
            'order': order,
            'profile': profile,
            'experiment': experiment,
            'user_samples': user_samples,
            'user_tests': user_tests,
            'current_step': 3

        }
        return context
    
    def form_valid(self, form):
        test_info = form.save(commit=False)
        order_code = self.kwargs.get('order_code')  # دریافت order_code از URL
        order = get_object_or_404(Order, order_code=order_code)
        test_info.order = order

        parameter_values = {}
        for key, value in self.request.POST.items():
            if key not in form.cleaned_data:
                parameter_values[key] = value

        # حذف توکن CSRF از parameter_values
        if 'csrfmiddlewaretoken' in parameter_values:
            del parameter_values['csrfmiddlewaretoken']

        # پرینت برای بررسی مقادیر parameter_values
        print("Collected parameter values without CSRF token:", parameter_values)

        # ذخیره مقادیر به عنوان JSON
        test_info.parameter_values = json.dumps(parameter_values)

        # پرینت برای بررسی مقدار parameter_values قبل از ذخیره
        print("JSON parameter values to be saved:", test_info.parameter_values)

        test_info.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        logger.error("Form is invalid.")
        logger.error(form.errors)
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
    def get_success_url(self):
        return reverse_lazy('userpanel:index')
    def form_valid(self, form):
        discount_info = form.save(commit=False)
        order_code = self.kwargs.get('order_code')
        order = get_object_or_404(Order, order_code=order_code)
        discount_info.order = order
        order.is_complete = True
        order.save()
        discount_info.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        logger.error("Form is invalid.")
        logger.error(form.errors)  # Log the form errors
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_code = self.kwargs['order_code']
        context['order'] = get_object_or_404(Order,order_code = order_code)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        context['current_step']= 4

        return context
    

class UserOrderCancelView(View):
    template_name = 'userpanel/order_confirm_cancel.html'
    success_url = reverse_lazy('userpanel:experiments-list')

    def get(self, request, order_code):
        order = get_object_or_404(Order, order_code=order_code)
        profile = Profile.objects.get(user=self.request.user)
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