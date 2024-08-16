from django.contrib.auth.views import LogoutView,LoginView
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.views.generic import FormView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

class LoginView(LoginView):
    def form_valid(self, form):
        messages.success(self.request, "شما با موفقیت وارد سایت  شدید.")
        return super().form_valid(form)

class LogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "شما با موفقیت از سایت خارج شدید.")
        return super().dispatch(request, *args, **kwargs)

class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request,"ثبت نام با موفقیت انجام شد")
        return super().form_valid(form)
    