from django.urls import path
from .views import *

app_name = 'orders'

urlpatterns = [
    path('create/<int:pk>', RequestTemplateView.as_view(), name='request-create'),
]