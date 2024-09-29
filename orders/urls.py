from django.urls import path
from .views import *

app_name = 'orders'

urlpatterns = [
    path('request-info/<int:experiment_id>/', RequestInfoCreateView.as_view(), name='request_info'),
    path('experiment/<int:experiment_id>/samples/', SampleInfoCreateView.as_view(), name='sample_info_create'),
]