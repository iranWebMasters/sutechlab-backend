from django.urls import path
from .views import *

app_name = 'orders'

urlpatterns = [
    path('request-info/<int:experiment_id>/', RequestInfoCreateView.as_view(), name='request_info'),
    path('experiment/<int:experiment_id>/samples/', SampleInfoCreateView.as_view(), name='sample_info_create'),
    path('samples/<int:id>/', SampleDetailView.as_view(), name='sample_detail'),
    path('samples/<int:id>/edit/', SampleEditView.as_view(), name='sample_edit'),
    path('samples/<int:id>/delete/', SampleDeleteView.as_view(), name='sample_delete'),
]