from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from accounts.models import Profile


class Indexview(TemplateView):
    template_name = 'userpanel/index.html'
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            profile = Profile.objects.get(user = request.user)
            required_fields = [profile.first_name, profile.last_name, profile.national_id, 
                           profile.phone_number, profile.address, profile.postal_code]
            if not all(required_fields):
                return redirect('accounts:update_profile')
        return super().dispatch(request, *args, **kwargs)