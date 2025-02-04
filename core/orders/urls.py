from django.urls import path
from .views import *

app_name = 'orders'

urlpatterns = [
    path('request-info/<int:experiment_id>/', OrderCreateView.as_view(), name='request_info'),
    path('request-info/update/<int:experiment_id>/', OrderUpdateView.as_view(), name='update_request_info'),
    path('experiment/<int:order_code>/samples/', SampleInfoCreateView.as_view(), name='sample_info_create'),
    path('samples/<int:pk>/', SampleDetailView.as_view(), name='sample_detail'),
    path('samples/edit/<int:pk>/', SampleEditView.as_view(), name='sample_edit'),
    path('experiment/<int:order_code>/samples/<int:pk>/delete/', SampleDeleteView.as_view(), name='sample_delete'),
    
    path('experiment/<int:order_code>/test-information/', TestInfoCreateView.as_view(), name='test_info_create'),
    path('get-parameters/<int:test_id>/', TestParametersView.as_view(), name='get_test_parameters'),
    path('parameters/<int:parameter_id>/values/',ParameterValuesView.as_view(),name = 'parameter_values'),
    path('test/<int:pk>/', TestDetailView.as_view(), name='test_detail'),
    path('test/<int:pk>/<int:experiment_id>/test/edit/', TestUpdateView.as_view(), name='test_edit'),
    path('experiment/<int:experiment_id>/test/<int:pk>/delete/', TestDeleteView.as_view(), name='test_delete'),

    path('discount-info/<int:order_code>/', DiscountInfoFormView.as_view(), name='discount_info'),
    path('confirm_cancel/<int:order_code>/',UserOrderCancelView.as_view(),name='confirm_cancel'),

]