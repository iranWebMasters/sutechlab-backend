from django.urls import path
from .views import *

app_name = 'orders'

urlpatterns = [
    path('request-info/<int:pk>/', RequestInfoCreateView.as_view(), name='request_info'),
    path('experiment/<int:pk>/update-description/', RequestInfoUpdateView.as_view(), name='request_info_update'),

    path('experiment/<int:experiment_id>/samples/', SampleInfoCreateView.as_view(), name='sample_info_create'),

    path('samples/<int:pk>/', SampleDetailView.as_view(), name='sample_detail'),
    path('samples/edit/<int:pk>/', SampleEditView.as_view(), name='sample_edit'),

    path('experiment/<int:experiment_id>/samples/<int:pk>/delete/', SampleDeleteView.as_view(), name='sample_delete'),
    
    path('experiment/<int:experiment_id>/test-information/', TestInformationView.as_view(), name='test_information'),
]