
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RequestInfoForm, SampleInfoForm, ExperimentInfoForm, AdditionalInfoForm, DiscountInfoForm
from .models import *
from django.urls import reverse_lazy






class ExperimentDetailView(View):
    def get(self, request, pk):
        experiment = get_object_or_404(Experiment, pk=pk)
        request_info_form = RequestInfoForm(user=request.user)
        sample_info_form = SampleInfoForm()
        experiment_info_form = ExperimentInfoForm()
        additional_info_form = AdditionalInfoForm()
        discount_info_form = DiscountInfoForm()
        template_name = 'requests/test/request_form.html'
        return render(request,self.template_name, {
            'request_info_form': request_info_form,
            'sample_info_form': sample_info_form,
            'experiment_info_form': experiment_info_form,
            'additional_info_form': additional_info_form,
            'discount_info_form': discount_info_form,
            'experiment': experiment,  # ارسال آزمایش به الگو
            'first_name': request.user.profile.first_name,
            'last_name': request.user.profile.last_name,
        })

    def post(self, request, pk):
        experiment = get_object_or_404(Experiment, pk=pk)
        request_info_form = RequestInfoForm(request.POST, user=request.user)
        sample_info_form = SampleInfoForm(request.POST)
        experiment_info_form = ExperimentInfoForm(request.POST)
        additional_info_form = AdditionalInfoForm(request.POST)
        discount_info_form = DiscountInfoForm(request.POST)

        if request_info_form.is_valid() and sample_info_form.is_valid() and \
           experiment_info_form.is_valid() and additional_info_form.is_valid() and \
           discount_info_form.is_valid():
            
            request_info = request_info_form.save(commit=False)
            request_info.experiment = experiment  # تنظیم آزمایش به آزمایش جاری
            request_info.save()
            
            sample_info = sample_info_form.save()
            experiment_info = experiment_info_form.save()
            additional_info = additional_info_form.save()
            discount_info = discount_info_form.save()

            request_instance = Request.objects.create(
                RequestInfo=request_info,
                SampleInfo=sample_info,
                ExperimentInfo=experiment_info,
                AdditionalInfo=additional_info
            )
            
            discount_info.request = request_instance
            discount_info.save()
            
            return redirect('request_list')  # Redirect to the list view

        return render(request,self.template_name, {
            'request_info_form': request_info_form,
            'sample_info_form': sample_info_form,
            'experiment_info_form': experiment_info_form,
            'additional_info_form': additional_info_form,
            'discount_info_form': discount_info_form,
            'experiment': experiment,  # ارسال آزمایش به الگو
            'first_name': request.user.profile.first_name,
            'last_name': request.user.profile.last_name,
        })



# Create Request
class RequestCreateView(CreateView):
    model = Request
    template_name = 'requests/test/request_form.html'
    
    def get(self, request, *args, **kwargs):
        request_info_form = RequestInfoForm()
        sample_info_form = SampleInfoForm()
        experiment_info_form = ExperimentInfoForm()
        additional_info_form = AdditionalInfoForm()
        discount_info_form = DiscountInfoForm()
        
        return render(request, self.template_name, {
            'request_info_form': request_info_form,
            'sample_info_form': sample_info_form,
            'experiment_info_form': experiment_info_form,
            'additional_info_form': additional_info_form,
            'discount_info_form': discount_info_form,
        })

    def post(self, request, *args, **kwargs):
        request_info_form = RequestInfoForm(request.POST)
        sample_info_form = SampleInfoForm(request.POST)
        experiment_info_form = ExperimentInfoForm(request.POST)
        additional_info_form = AdditionalInfoForm(request.POST)
        discount_info_form = DiscountInfoForm(request.POST)

        if request_info_form.is_valid() and sample_info_form.is_valid() and \
           experiment_info_form.is_valid() and additional_info_form.is_valid() and \
           discount_info_form.is_valid():
            
            request_info = request_info_form.save()
            sample_info = sample_info_form.save()
            experiment_info = experiment_info_form.save()
            additional_info = additional_info_form.save()
            discount_info = discount_info_form.save()

            request_instance = Request.objects.create(
                RequestInfo=request_info,
                SampleInfo=sample_info,
                ExperimentInfo=experiment_info,
                AdditionalInfo=additional_info
            )
            
            discount_info.request = request_instance
            discount_info.save()
            
            return redirect('request_list')  # Redirect to the list view

        return render(request, self.template_name, {
            'request_info_form': request_info_form,
            'sample_info_form': sample_info_form,
            'experiment_info_form': experiment_info_form,
            'additional_info_form': additional_info_form,
            'discount_info_form': discount_info_form,
        })

# List Requests
class RequestListView(ListView):
    model = Request
    template_name = 'request_list.html'
    context_object_name = 'requests'

# Update Request
class RequestUpdateView(UpdateView):
    model = Request
    template_name = 'request_form.html'
    form_class = RequestInfoForm  # You can use a custom form for the entire request if needed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sample_info_form'] = SampleInfoForm(instance=self.object.SampleInfo)
        context['experiment_info_form'] = ExperimentInfoForm(instance=self.object.ExperimentInfo)
        context['additional_info_form'] = AdditionalInfoForm(instance=self.object.AdditionalInfo)
        context['discount_info_form'] = DiscountInfoForm(instance=self.object.DiscountInfo)
        return context

    def form_valid(self, form):
        request_info = form.save()
        sample_info_form = SampleInfoForm(self.request.POST, instance=self.object.SampleInfo)
        experiment_info_form = ExperimentInfoForm(self.request.POST, instance=self.object.ExperimentInfo)
        additional_info_form = AdditionalInfoForm(self.request.POST, instance=self.object.AdditionalInfo)
        discount_info_form = DiscountInfoForm(self.request.POST, instance=self.object.DiscountInfo)

        if sample_info_form.is_valid() and experiment_info_form.is_valid() and \
           additional_info_form.is_valid() and discount_info_form.is_valid():
            sample_info_form.save()
            experiment_info_form.save()
            additional_info_form.save()
            discount_info_form.save()
            return redirect('request_list')
        
        return self.render_to_response(self.get_context_data(form=form))

# Delete Request
class RequestDeleteView(DeleteView):
    model = Request
    template_name = 'request_confirm_delete.html'
    success_url = reverse_lazy('request_list')