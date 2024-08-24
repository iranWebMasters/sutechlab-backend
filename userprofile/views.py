from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.



class ProfileIndexview(TemplateView):
    template_name = 'profile/index.html'