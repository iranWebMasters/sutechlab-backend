from django.contrib.auth.views import LogoutView,LoginView
from django.contrib import messages
from django.shortcuts import redirect

class LoginView(LoginView):
    def form_valid(self, form):
        messages.success(self.request, "شما با موفقیت وارد سایت  شدید.")
        return super().form_valid(form)

class LogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "شما با موفقیت از سایت خارج شدید.")
        return super().dispatch(request, *args, **kwargs)
