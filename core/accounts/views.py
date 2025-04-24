from django.contrib.auth.views import (
    LogoutView,
    LoginView,
    PasswordResetView,
    PasswordResetConfirmView,
)
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.views.generic import UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import FormView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import *
from .models import Profile


class LoginView(LoginView):
    def form_valid(self, form):
        messages.success(self.request, "شما با موفقیت وارد سایت شدید.")
        return super().form_valid(form)

    def form_invalid(self, form):
        for field in form:
            for error in field.errors:
                messages.error(self.request, f"Error in field '{field.label}': {error}")
        for error in form.non_field_errors():
            messages.error(self.request, f"Non-field error: {error}")

        return super().form_invalid(form)


class LogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.warning(request, "شما از حساب کاربری خود خارج شدید.")
        return super().dispatch(request, *args, **kwargs)


class RegisterView(FormView):
    template_name = "registration/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "ثبت نام با موفقیت انجام شد")
        return super().form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = "registration/update_profile.html"
    success_url = reverse_lazy("userpanel:index")

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "پروفایل شما با موفقیت بروز رسانی شد.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "خطایی در بروز رسانی پروفایل شما رخ داد.")
        response = super().form_invalid(form)
        return response


class PasswordResetView(PasswordResetView):
    template_name = "registration/password_reset.html"
    email_template_name = "registration/password_reset_email.html"
    subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")

    def form_valid(self, form):
        messages.success(self.request, "لینک بازنشانی رمز عبور به ایمیل شما ارسال شد.")
        return super().form_valid(form)


class PasswordResetDoneView(TemplateView):
    template_name = "registration/password_reset_done.html"


class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")

    def form_valid(self, form):
        messages.success(self.request, "رمز عبور شما با موفقیت تغییر کرد.")
        return super().form_valid(form)


class PasswordResetCompleteView(TemplateView):
    template_name = "registration/password_reset_complete.html"
