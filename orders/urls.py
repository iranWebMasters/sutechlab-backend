from django.urls import path
from .views import *

app_name = 'orders'

urlpatterns = [
    path('experiment/<int:pk>/', ExperimentDetailView.as_view(), name='request_detail'),
    path('create-request/', RequestCreateView.as_view(), name='create_request'),
    path('requests/', RequestListView.as_view(), name='request_list'),
    path('request/<int:pk>/update/', RequestUpdateView.as_view(), name='request_update'),
    path('request/<int:pk>/delete/', RequestDeleteView.as_view(), name='request_delete'),
]