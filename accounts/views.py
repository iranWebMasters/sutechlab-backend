from django.contrib.auth.views import LogoutView,LoginView
from django.http import HttpResponse
from django.views.generic import FormView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm

class LoginView(LoginView):
    def form_valid(self, form):
        messages.success(self.request, "شما با موفقیت وارد سایت  شدید.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # ثبت ارورهای فرم به سیستم پیام‌ها
        for field in form:
            for error in field.errors:
                messages.error(self.request, f"Error in field '{field.label}': {error}")
        for error in form.non_field_errors():
            messages.error(self.request, f"Non-field error: {error}")

        # ادامه‌ی عملکرد پیش‌فرض
        return super().form_invalid(form)

class LogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.warning(request, "شمااز سایت خارج شدید.")
        return super().dispatch(request, *args, **kwargs)

class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request,"ثبت نام با موفقیت انجام شد")
        return super().form_valid(form)
    