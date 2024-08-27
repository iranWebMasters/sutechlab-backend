from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.



class Indexview(TemplateView):
    template_name = 'userpanel/index.html'